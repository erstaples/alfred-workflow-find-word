# Find Word - Alfred Workflow

A reverse dictionary Alfred workflow powered by Claude AI. Find words based on their meanings or descriptions, with optional literary mode for more sophisticated vocabulary.

<img src="https://via.placeholder.com/512x512.png?text=Find+Word" width="128" alt="Find Word Icon">

## Features

- **Reverse Dictionary Lookup**: Describe what you mean, get word suggestions
- **Literary Mode**: Get more sophisticated, eloquent word suggestions
- **Smart Definitions**: Each word comes with a concise definition
- **Fast Results**: Powered by Claude AI for intelligent matching

## Installation

### 1. Clone or Download

```bash
cd ~/code/misc
git clone https://github.com/yourusername/find-word-alfred-plugin.git
# or download and extract the zip
```

### 2. Install Python Dependencies

```bash
pip3 install anthropic
```

### 3. Build and Import to Alfred

Build the workflow package and install it:

```bash
cd find-word-alfred-plugin
make install
```

This will create `Find Word.alfredworkflow` and open it for installation in Alfred.

Alternatively, you can:
- Run `make build` to just create the package
- Double-click `Find Word.alfredworkflow` manually to install

### 4. Get Your Claude API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign in or create an account
3. Navigate to **API Keys** in the left sidebar
4. Click **Create Key**
5. Give it a name (e.g., "Alfred Find Word")
6. Copy the API key (you won't be able to see it again!)

### 5. Configure Environment Variables in Alfred

After importing the workflow and getting your API key:

1. Open Alfred Preferences → Workflows
2. Select the "Find Word" workflow
3. Click the **[x]** button in the top right corner (Configure Workflow)
4. Set the following variables:
   - **Name**: `ANTHROPIC_API_KEY`
   - **Value**: Paste your API key from step 4 above

5. (Optional) Add another variable for a different model:
   - **Name**: `CLAUDE_MODEL`
   - **Value**: `claude-3-5-sonnet-20240620` (or [another model](https://docs.claude.com/en/docs/about-claude/models/overview#choosing-a-model))
   - Leave blank to use the default: `claude-haiku-4-5-20251001`

## Usage

### Regular Mode
```
find-word to make unnecessary
```
Returns: `obviate`, `preclude`, `eliminate`, etc.

### Literary Mode
```
find-word-lit sad
```
Returns: `melancholy`, `wistful`, `forlorn`, `plaintive`, etc.

## Examples

| Query | Results |
|-------|---------|
| `find-word to make worse` | exacerbate, aggravate, worsen |
| `find-word-lit beautiful` | resplendent, pulchritudinous, ethereal |
| `find-word brief and to the point` | concise, succinct, terse, laconic |
| `find-word-lit peaceful` | serene, tranquil, halcyon, placid |

## How It Works

1. You type a description of the word you're looking for
2. The workflow sends your description to Claude AI
3. Claude analyzes your description and returns relevant words
4. In literary mode, Claude prioritizes sophisticated, eloquent vocabulary
5. Each word is returned with a concise definition
6. Results are ranked by relevance to your description

## Configuration

### Adjusting Number of Results

Edit `find_word.py` and modify the system prompt:

```python
system_prompt = f"""...
Provide 5-10 words ranked by relevance."""  # Change to your preferred range
```

### Changing Claude Model

To use a different Claude model:

1. Open Alfred Preferences → Workflows
2. Select "Find Word" workflow
3. Click the **[x]** button (Configure Workflow)
4. Add or edit the `CLAUDE_MODEL` variable
5. Set it to one of the available models below

Available models:
- `claude-haiku-4-5-20251001` (default, fast and cheap)
- `claude-3-5-sonnet-20240620` (more capable, balanced)
- `claude-3-opus-20240229` (most capable, slower, more expensive)
- `claude-3-haiku-20240307` (older haiku version)

For detailed information about model capabilities, performance, and pricing, see the [Claude Models Overview](https://docs.claude.com/en/docs/about-claude/models/overview#choosing-a-model).

## Troubleshooting

### "anthropic package not installed"
Run: `pip3 install anthropic`

### "ANTHROPIC_API_KEY environment variable not set"
1. Open Alfred Preferences → Workflows → Find Word
2. Click the **[x]** button (Configure Workflow)
3. Verify `ANTHROPIC_API_KEY` is set with your API key
4. If you just added it, restart Alfred completely (quit and reopen)

### No results or errors
1. Check your API key is valid
2. Verify you have API credits remaining
3. Check your internet connection
4. View Alfred's debug console (workflow view → bug icon)

## Customization

### Adding an Icon

Add an `icon.png` file (512x512 recommended) to the workflow folder. Alfred will automatically use it.

### Modifying Keywords

Edit `info.plist` and change the `<key>keyword</key>` values under each script filter object.

## Development

### Building the Workflow

The project includes a Makefile for easy workflow management:

```bash
make build    # Build the workflow package
make clean    # Remove the workflow package
make install  # Build and open for installation
make help     # Show available commands
```

## Cost Considerations

This workflow uses the Claude API, which is paid:
- Each query with Claude Haiku 4.5 (default) costs approximately $0.0001-0.0003
- For better quality results, use Claude 3.5 Sonnet (~$0.001-0.003 per query)
- The default Haiku model provides great results at minimal cost

## Contributing

Issues and pull requests welcome!

## License

MIT License - feel free to modify and share

## Credits

Created by estaples
Powered by [Anthropic Claude](https://www.anthropic.com/)
