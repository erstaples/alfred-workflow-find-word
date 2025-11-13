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

Return your response as a JSON array of objects with these fields:
- word: the suggested word
- definition: concise definition (1-2 sentences)
- part_of_speech: one of "noun", "verb", "adjective", "adverb", "preposition", "conjunction", "interjection"
- frequency: number 1-10 (10=very common, 1=very rare)
- origin: language of origin (e.g., "Latin", "Greek", "French", "Germanic", "Arabic")
- etymology: brief etymology (1 sentence, how the word came to be)
- synonyms: array of 2-4 related words with similar meaning
- antonyms: array of 1-3 words with opposite meaning (or empty array if none)

Example format:
[
  {{
    "word": "obviate",
    "definition": "To remove or prevent (a need or difficulty); make unnecessary.",
    "part_of_speech": "verb",
    "frequency": 3,
    "origin": "Latin",
    "etymology": "From Latin 'obviatus', meaning 'to meet or counter'.",
    "synonyms": ["preclude", "prevent", "avert", "forestall"],
    "antonyms": ["necessitate", "require"]
  }}
]

Provide 5-10 words ranked by relevance."""

    try:
        client = anthropic.Anthropic(api_key=api_key)

        # Get model from environment variable or use default
        model = os.environ.get('CLAUDE_MODEL', 'claude-haiku-4-5-20251001')

        message = client.messages.create(
            model=model,
            max_tokens=2048,
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


def get_pos_abbreviation(part_of_speech: str) -> str:
    """Get clear text abbreviation for part of speech."""
    abbreviations = {
        'noun': 'n',
        'verb': 'v',
        'adjective': 'adj',
        'adverb': 'adv',
        'preposition': 'prep',
        'conjunction': 'conj',
        'interjection': 'interj',
        'pronoun': 'pron'
    }
    abbr = abbreviations.get(part_of_speech.lower(), part_of_speech[:4])
    return f"({abbr})"


def get_origin_flag(origin: str) -> str:
    """Get flag emoji for word origin."""
    origin_lower = origin.lower()
    flags = {
        'latin': '🇻🇦',
        'greek': '🇬🇷',
        'french': '🇫🇷',
        'germanic': '🇩🇪',
        'german': '🇩🇪',
        'arabic': '🇸🇦',
        'spanish': '🇪🇸',
        'italian': '🇮🇹',
        'portuguese': '🇵🇹',
        'russian': '🇷🇺',
        'chinese': '🇨🇳',
        'japanese': '🇯🇵',
        'old english': '🇬🇧',
        'english': '🇬🇧',
        'dutch': '🇳🇱',
        'sanskrit': '🇮🇳',
        'hebrew': '🇮🇱',
        'persian': '🇮🇷'
    }
    return flags.get(origin_lower, '🌍')


def create_alfred_items(words: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Convert word results to Alfred Script Filter JSON format.

    Args:
        words: List of word objects with enhanced metadata

    Returns:
        List of Alfred item objects
    """
    items = []

    for idx, word_obj in enumerate(words):
        word = word_obj.get('word', '')
        definition = word_obj.get('definition', 'No definition available')
        part_of_speech = word_obj.get('part_of_speech', '')
        frequency = word_obj.get('frequency', 5)
        origin = word_obj.get('origin', 'Unknown')
        etymology = word_obj.get('etymology', '')
        synonyms = word_obj.get('synonyms', [])
        antonyms = word_obj.get('antonyms', [])

        # Build enhanced title with POS abbreviation and subtle frequency bar
        pos_abbr = get_pos_abbreviation(part_of_speech)
        # Use subtle dots for frequency (filled vs empty)
        freq_bars = '●' * min(frequency, 10)
        freq_bars += '○' * (10 - min(frequency, 10))
        title = f"{pos_abbr} {word}  {freq_bars}"

        # Build enhanced subtitle with just the definition
        subtitle = definition

        # Get origin flag for etymology view
        origin_flag = get_origin_flag(origin)

        # Format synonyms and antonyms for modifiers
        synonyms_text = ", ".join(synonyms) if synonyms else "No synonyms available"
        antonyms_text = ", ".join(antonyms) if antonyms else "No antonyms available"

        # Format etymology with origin
        etymology_text = f"{origin_flag} {origin} • {etymology}" if etymology else f"{origin_flag} {origin}"

        item = {
            'uid': f"find-word-{word}-{idx}",
            'title': title,
            'subtitle': subtitle,
            'arg': word,
            'autocomplete': word,
            'valid': True,
            'text': {
                'copy': word,
                'largetype': f"{word}\n\n{definition}"
            },
            'mods': {
                'shift': {
                    'valid': True,
                    'arg': word,
                    'subtitle': f"Synonyms: {synonyms_text} | Antonyms: {antonyms_text}"
                },
                'ctrl': {
                    'valid': True,
                    'arg': word,
                    'subtitle': etymology_text
                }
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
            items = create_alfred_items(words)
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
