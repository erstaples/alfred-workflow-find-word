#!/usr/bin/env python3
"""
Alfred workflow for reverse dictionary lookup using Claude API.
Finds words based on their meanings/descriptions with optional literary mode.
"""

import json
import sys
import os
from typing import List, Dict, Any


def query_claude(description: str, literary: bool = False) -> List[Dict[str, str]]:
    """
    Query Claude API for word suggestions based on description.

    Args:
        description: The description or meaning to search for
        literary: Whether to prefer literary/flowery language

    Returns:
        List of dicts with 'word' and 'definition' keys
    """
    try:
        import anthropic
    except ImportError:
        return [{
            'word': 'Error',
            'definition': 'anthropic package not installed. Run: pip3 install anthropic'
        }]

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return [{
            'word': 'Error',
            'definition': 'ANTHROPIC_API_KEY environment variable not set'
        }]

    literary_instruction = ""
    if literary:
        literary_instruction = " Prefer sophisticated, literary, or eloquent words that would be appropriate in formal or creative writing."

    system_prompt = f"""You are a reverse dictionary assistant. Given a description or meaning, suggest words that match it.{literary_instruction}

Return your response as a JSON array of objects, each with 'word' and 'definition' fields.
The definition should be concise (1-2 sentences) and include the part of speech in brackets.

Example format:
[
  {{"word": "obviate", "definition": "[verb] To remove or prevent (a need or difficulty); make unnecessary."}},
  {{"word": "preclude", "definition": "[verb] To prevent from happening; make impossible."}}
]

Provide 5-10 words ranked by relevance."""

    try:
        client = anthropic.Anthropic(api_key=api_key)

        # Get model from environment variable or use default
        model = os.environ.get('CLAUDE_MODEL', 'claude-haiku-4-5-20251001')

        message = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": description
            }],
            system=system_prompt
        )

        # Extract the text response
        response_text = message.content[0].text

        # Parse JSON from response
        # Claude might wrap it in markdown code blocks, so let's handle that
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        words = json.loads(response_text)
        return words

    except anthropic.APIError as e:
        return [{
            'word': 'API Error',
            'definition': f'Claude API error: {str(e)}'
        }]
    except json.JSONDecodeError as e:
        return [{
            'word': 'Parse Error',
            'definition': f'Could not parse Claude response: {str(e)}'
        }]
    except Exception as e:
        return [{
            'word': 'Error',
            'definition': f'Unexpected error: {str(e)}'
        }]


def create_alfred_items(words: List[Dict[str, str]], query: str) -> List[Dict[str, Any]]:
    """
    Convert word results to Alfred Script Filter JSON format.

    Args:
        words: List of word objects with 'word' and 'definition' keys
        query: Original search query

    Returns:
        List of Alfred item objects
    """
    items = []

    for idx, word_obj in enumerate(words):
        word = word_obj.get('word', '')
        definition = word_obj.get('definition', 'No definition available')

        item = {
            'uid': f"find-word-{word}-{idx}",
            'title': word,
            'subtitle': definition,
            'arg': word,
            'autocomplete': word,
            'valid': True,
            'text': {
                'copy': word,
                'largetype': f"{word}\n\n{definition}"
            }
        }

        items.append(item)

    return items


def main():
    """Main entry point for the Alfred workflow."""
    # Determine if literary mode is enabled based on script name or first argument
    literary = False
    args = sys.argv[1:]

    # Check if running with literary mode (script can be called with different names)
    script_name = os.path.basename(sys.argv[0])
    if 'lit' in script_name or (args and args[0] == '--literary'):
        literary = True
        if args and args[0] == '--literary':
            args = args[1:]  # Remove the flag from args

    # Get query from Alfred (passed as command line arguments)
    query = ' '.join(args) if args else ''

    if not query or len(query.strip()) < 2:
        # Show placeholder when query is too short
        mode_text = "literary " if literary else ""
        output = {
            'items': [{
                'title': f'Find {mode_text.title()}Word by Meaning',
                'subtitle': f'Type a description of the {mode_text}word you\'re looking for...',
                'valid': False
            }]
        }
    else:
        # Query Claude API
        words = query_claude(query, literary=literary)

        if words:
            items = create_alfred_items(words, query)
            output = {'items': items}
        else:
            output = {
                'items': [{
                    'title': 'No Results Found',
                    'subtitle': f'No words found matching "{query}"',
                    'valid': False
                }]
            }

    # Output JSON for Alfred
    print(json.dumps(output, ensure_ascii=False))


if __name__ == '__main__':
    main()
