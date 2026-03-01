# PollenClub VK Comment Analyzer

A tool for collecting and analyzing comments from the [PollenClub](https://vk.com/pollenclub) VK community. It fetches wall posts, filters survey posts about well-being, extracts toponyms (cities, regions) from comments, and produces a CSV report.

## How It Works

1. **Fetch posts** — retrieves the latest wall posts from the group via VK API.
2. **Filter** — keeps only posts where the author asks subscribers to report their well-being along with their geolocation.
3. **Fetch comments** — downloads direct comments (excluding replies) for each relevant post.
4. **Extract toponyms** — using the [yargy](https://github.com/natasha/yargy) library and the [pymorphy2](https://pymorphy2.readthedocs.io/) morphological analyzer, the following entities are extracted from each comment:
   - City
   - Republic
   - Krai
   - Oblast
   - Okrug
   - Moscow district
5. **Export** — results are saved to a CSV file named `report_DD_MM_YYYY_HH_MM_SS.csv` in the `/data` directory.

## Project Structure

```
PollenClub/
├── src/
│   ├── app.py               # Entry point
│   ├── vk_parser.py         # VK API parser
│   ├── utils.py             # Helper utilities
│   └── extractor/
│       ├── main.py          # Toponym extraction orchestrator
│       ├── toponim_parser_yargo.py  # Toponym parser (yargy)
│       ├── yargo_rules.py   # yargy grammars
│       └── dict/            # Russian city and region dictionaries
├── data/                    # Input comments and output reports
├── env/                     # .env file with VK token
├── Dockerfile
├── Makefile
└── pyproject.toml
```

## Requirements

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- VK API token with read access to wall posts and comments

## Installation & Usage

### Local

```bash
# Install dependencies
uv sync

# Create the token file
echo "VK_TOKEN=your_token_here" > env/.env

# Run
uv run python src/app.py --vk_token your_token_here
# or via environment variable
export VK_TOKEN=your_token_here
uv run python src/app.py
```

### Docker

```bash
# Build the image
make build

# Run (token is read from env/.env)
make run
```

Output files will be saved to the `data/` folder on the host.

### Pre-built image from Docker Hub

```bash
docker pull physci/pollenclub:latest
docker run --rm -it \
    -v "$(pwd)"/data:/data \
    --env-file "$(pwd)"/env/.env \
    physci/pollenclub:latest
```

## Configuration

| Variable | Description |
|---|---|
| `VK_TOKEN` | VK API token (required) |

The token can be provided via the `env/.env` file, an environment variable, or the `--vk_token` CLI argument.

## Output Format

The `report_*.csv` file contains the following fields:

| Field | Description |
|---|---|
| `datetime` | Comment date and time |
| `user_name` | User's first and last name |
| `msg` | Comment text |
| `city` | Extracted city |
| `resp` | Republic |
| `krai` | Krai |
| `obl` | Oblast |
| `okr` | Okrug |
| `msk_r` | Moscow district |
| `drugs` | Mentioned medications |
| `symptoms` | Symptoms |
| `allergens` | Allergens |

## CI/CD

The project uses GitHub Actions to automatically build and publish the Docker image to Docker Hub (`physci/pollenclub`):

- **dev** — triggered on push to any branch except `master` → tagged as `dev`
- **master** — triggered on push to `master` → tagged as `latest` and with a version tag

## Tech Stack

- [vkbottle](https://github.com/vkbottle/vkbottle) — async VK API client
- [yargy](https://github.com/natasha/yargy) — named entity extraction
- [pymorphy2](https://pymorphy2.readthedocs.io/) — Russian morphological analysis
- [pandas](https://pandas.pydata.org/) — tabular data processing

## Based On

This project builds upon the following prior works:

- [Dehle/Finding-toponyms-from-the-text](https://github.com/Dehle/Finding-toponyms-from-the-text) — toponym extraction from community messages using yargy
- [Den1079/polen_club](https://github.com/Den1079/polen_club) — VK comment parser for the PollenClub group
- [dimdasci/m02-export-vk-comments](https://github.com/dimdasci/m02-export-vk-comments) — VK wall comments export tool
- [dataMasterskaya/PollenClub_parser](https://github.com/dataMasterskaya/PollenClub_parser) — PollenClub community comment parser
