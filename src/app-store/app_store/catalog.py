import json
import re
import ssl
import urllib.error
import urllib.request


APP_CATALOG = {
    "automatic1111": {
        "description": "Stable Diffusion WebUI for image generation.",
        "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
        "version": "v1.10.0",
        "latest": {"type": "github-release", "repo": "AUTOMATIC1111/stable-diffusion-webui"},
    },
    "comfyui": {
        "description": "Node-based Stable Diffusion workflow UI.",
        "url": "https://github.com/comfyanonymous/ComfyUI",
        "version": "v0.2.2",
        "latest": {"type": "github-release", "repo": "comfyanonymous/ComfyUI"},
    },
    "discourse": {
        "description": "Forum and community discussion platform.",
        "url": "https://www.discourse.org/",
        "version": "3.3.2",
        "latest": {"type": "github-tags", "repo": "discourse/discourse"},
    },
    "docuseal": {
        "description": "Open-source document signing platform.",
        "url": "https://www.docuseal.com/",
        "version": "1.7.5",
        "latest": {"type": "github-release", "repo": "docusealco/docuseal"},
    },
    "erpnext": {
        "description": "ERP suite for accounting, inventory, HR, CRM, and operations.",
        "url": "https://erpnext.com/",
        "version": "15.57.5",
        "latest": {"type": "github-release", "repo": "frappe/erpnext"},
    },
    "espocrm": {
        "description": "Open-source CRM for sales and customer management.",
        "url": "https://www.espocrm.com/",
        "version": "9.3.7",
        "latest": {"type": "github-release", "repo": "espocrm/espocrm"},
    },
    "faster-whisper-server": {
        "description": "OpenAI-compatible speech-to-text API backed by faster-whisper.",
        "url": "https://github.com/fedirz/faster-whisper-server",
        "version": "0.5.0-cuda",
        "latest": {"type": "github-release", "repo": "fedirz/faster-whisper-server"},
    },
    "flowise": {
        "description": "Low-code builder for LLM and agent workflows.",
        "url": "https://flowiseai.com/",
        "version": "2.1.2",
        "latest": {
            "type": "github-release",
            "repo": "FlowiseAI/Flowise",
            "strip_prefix": "flowise@",
        },
    },
    "frappe-crm": {
        "description": "CRM built on the Frappe framework.",
        "url": "https://github.com/frappe/crm",
        "version": "15",
        "latest": {"type": "github-tags", "repo": "frappe/crm"},
    },
    "gitea": {
        "description": "Self-hosted Git service for repositories, issues, and CI.",
        "url": "https://about.gitea.com/",
        "version": "1.21.4",
        "latest": {"type": "github-release", "repo": "go-gitea/gitea"},
    },
    "immich": {
        "description": "Self-hosted photo and video backup service.",
        "url": "https://immich.app/",
        "version": "v1.117.0",
        "latest": {"type": "github-release", "repo": "immich-app/immich"},
    },
    "keycloak": {
        "description": "Identity and access management server.",
        "url": "https://www.keycloak.org/",
        "version": "21.0",
        "latest": {"type": "github-release", "repo": "keycloak/keycloak"},
    },
    "langflow": {
        "description": "Visual builder for AI agents and LangChain-style workflows.",
        "url": "https://www.langflow.org/",
        "version": "1.4.1",
        "latest": {"type": "github-release", "repo": "langflow-ai/langflow"},
    },
    "langfuse": {
        "description": "LLM observability, tracing, evaluation, and prompt management.",
        "url": "https://langfuse.com/",
        "version": "3.28",
        "latest": {"type": "github-release", "repo": "langfuse/langfuse"},
    },
    "litellm": {
        "description": "OpenAI-compatible proxy for many LLM providers.",
        "url": "https://www.litellm.ai/",
        "version": "1.60.8",
        "latest": {
            "type": "github-release",
            "repo": "BerriAI/litellm",
            "strip_prefix": "v",
        },
    },
    "matrix": {
        "description": "Matrix Synapse homeserver with WhatsApp bridge components.",
        "url": "https://matrix.org/",
        "version": "1.116.0",
        "latest": {"type": "github-release", "repo": "element-hq/synapse"},
    },
    "mattermost": {
        "description": "Team chat and collaboration platform.",
        "url": "https://mattermost.com/",
        "version": "10.11.9",
        "latest": {"type": "github-release", "repo": "mattermost/mattermost"},
    },
    "mediacms": {
        "description": "Video and media publishing platform.",
        "url": "https://mediacms.io/",
        "version": "5.0.1",
        "latest": {"type": "github-release", "repo": "mediacms-io/mediacms"},
    },
    "metabase": {
        "description": "Business intelligence and analytics dashboards.",
        "url": "https://www.metabase.com/",
        "version": "0.55.4.4",
        "latest": {"type": "github-release", "repo": "metabase/metabase"},
    },
    "minio": {
        "description": "S3-compatible object storage server.",
        "url": "https://min.io/",
        "version": "2025-04-22T22-12-26Z",
        "latest": {"type": "dockerhub-release-tags", "repo": "minio/minio"},
    },
    "moodle": {
        "description": "Learning management system for courses and education.",
        "url": "https://moodle.org/",
        "version": "4.5",
        "latest": {"type": "github-tags", "repo": "moodle/moodle"},
    },
    "n8n": {
        "description": "Workflow automation and integration platform.",
        "url": "https://n8n.io/",
        "version": "2.17.0",
        "latest": {
            "type": "github-release",
            "repo": "n8n-io/n8n",
            "strip_prefix": "n8n@",
        },
    },
    "nocodb": {
        "description": "No-code database interface and Airtable alternative.",
        "url": "https://nocodb.com/",
        "version": "latest",
        "latest": {"type": "github-release", "repo": "nocodb/nocodb"},
    },
    "open-webui": {
        "description": "Web UI for local and remote LLMs.",
        "url": "https://github.com/open-webui/open-webui",
        "version": "0.6.2",
        "latest": {"type": "github-release", "repo": "open-webui/open-webui"},
    },
    "openedai-speech": {
        "description": "OpenAI-compatible text-to-speech API server.",
        "url": "https://github.com/matatonic/openedai-speech",
        "version": "0.18.2",
        "latest": {"type": "github-release", "repo": "matatonic/openedai-speech"},
    },
    "outline": {
        "description": "Team knowledge base and collaborative wiki.",
        "url": "https://www.getoutline.com/",
        "version": "0.81.1",
        "latest": {"type": "github-release", "repo": "outline/outline"},
    },
    "paperless-gpt": {
        "description": "AI assistant for Paperless document workflows.",
        "url": "https://github.com/icereed/paperless-gpt",
        "version": "0.5.1",
        "latest": {"type": "github-release", "repo": "icereed/paperless-gpt"},
    },
    "paperless-ngx": {
        "description": "Document management system for scanned paperwork.",
        "url": "https://docs.paperless-ngx.com/",
        "version": "2.14.7",
        "latest": {"type": "github-release", "repo": "paperless-ngx/paperless-ngx"},
    },
    "penpot": {
        "description": "Open-source design and prototyping platform.",
        "url": "https://penpot.app/",
        "version": "2.4.1",
        "latest": {"type": "github-release", "repo": "penpot/penpot"},
    },
    "pgadmin": {
        "description": "Web administration UI for PostgreSQL.",
        "url": "https://www.pgadmin.org/",
        "version": "9.3.0",
        "latest": {"type": "dockerhub-tags", "repo": "dpage/pgadmin4"},
    },
    "planka": {
        "description": "Kanban project management board.",
        "url": "https://planka.app/",
        "version": "1.24.3",
        "latest": {"type": "github-release", "repo": "plankanban/planka"},
    },
    "qdrant": {
        "description": "Vector database for semantic search and AI applications.",
        "url": "https://qdrant.tech/",
        "version": "v1.12.0",
        "latest": {"type": "github-release", "repo": "qdrant/qdrant"},
    },
    "shlink": {
        "description": "Self-hosted URL shortener.",
        "url": "https://shlink.io/",
        "version": "4.5.2",
        "latest": {"type": "github-release", "repo": "shlinkio/shlink"},
    },
    "snipe-it": {
        "description": "IT asset and license management system.",
        "url": "https://snipeitapp.com/",
        "version": "8.0.4",
        "latest": {"type": "github-release", "repo": "snipe/snipe-it"},
    },
    "thelounge": {
        "description": "Self-hosted web IRC client.",
        "url": "https://thelounge.chat/",
        "version": "4.4.3",
        "latest": {"type": "github-release", "repo": "thelounge/thelounge"},
    },
    "twenty": {
        "description": "Open-source CRM platform.",
        "url": "https://twenty.com/",
        "version": "0.31.2",
        "latest": {
            "type": "github-release",
            "repo": "twentyhq/twenty",
            "strip_prefix": "twenty/",
        },
    },
    "typebot": {
        "description": "Conversational form and chatbot builder.",
        "url": "https://typebot.io/",
        "version": "3.2.0",
        "latest": {"type": "github-release", "repo": "baptisteArno/typebot.io"},
    },
    "umami": {
        "description": "Privacy-focused web analytics.",
        "url": "https://umami.is/",
        "version": "3.1",
        "latest": {"type": "github-release", "repo": "umami-software/umami"},
    },
    "uptime-kuma": {
        "description": "Self-hosted uptime monitoring dashboard.",
        "url": "https://uptime.kuma.pet/",
        "version": "1.23.15",
        "latest": {"type": "github-release", "repo": "louislam/uptime-kuma"},
    },
    "vaultwarden": {
        "description": "Lightweight Bitwarden-compatible password manager server.",
        "url": "https://github.com/dani-garcia/vaultwarden",
        "version": "1.33.2",
        "latest": {"type": "github-release", "repo": "dani-garcia/vaultwarden"},
    },
    "vikunja": {
        "description": "Task and project management application.",
        "url": "https://vikunja.io/",
        "version": "0.24.6",
        "latest": {"type": "github-release", "repo": "go-vikunja/vikunja"},
    },
    "vllm": {
        "description": "High-throughput LLM inference server.",
        "url": "https://docs.vllm.ai/",
        "version": "0.6.2",
        "latest": {
            "type": "github-release",
            "repo": "vllm-project/vllm",
            "strip_prefix": "v",
        },
    },
}

latest_version_cache = {}


def _get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "johnny"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        if "CERTIFICATE_VERIFY_FAILED" not in str(exc):
            raise
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=8, context=context) as resp:
            return json.loads(resp.read().decode())


def _version_key(version):
    nums = re.findall(r"\d+", version)
    return tuple(int(n) for n in nums[:8])


def _latest_github_release(repo):
    data = _get_json(f"https://api.github.com/repos/{repo}/releases/latest")
    return data.get("tag_name") or data.get("name")


def _latest_github_tag(repo):
    data = _get_json(f"https://api.github.com/repos/{repo}/tags?per_page=100")
    tags = [item["name"] for item in data if re.search(r"\d", item.get("name", ""))]
    if not tags:
        return None
    return sorted(tags, key=_version_key)[-1]


def _latest_dockerhub_tag(repo, release_tags=False):
    data = _get_json(
        f"https://registry.hub.docker.com/v2/repositories/{repo}/tags?page_size=100"
    )
    tags = [item["name"] for item in data.get("results", [])]
    if release_tags:
        tags = [tag for tag in tags if tag.startswith("RELEASE.")]
    else:
        tags = [
            tag
            for tag in tags
            if re.match(
                r"^v?\d+(\.\d+){0,4}([.-](alpine|bookworm|debian|ubuntu|fpm|apache|rootless|cuda|oss|ce)\w*)?$",
                tag,
            )
        ]

    if not tags:
        return None
    return sorted(tags, key=_version_key)[-1]


def latest_version(app_name):
    if app_name in latest_version_cache:
        return latest_version_cache[app_name]

    app_data = APP_CATALOG.get(app_name, {})
    source = app_data.get("latest")
    latest = None
    if source:
        try:
            if source["type"] == "github-release":
                latest = _latest_github_release(source["repo"])
            elif source["type"] == "github-tags":
                latest = _latest_github_tag(source["repo"])
            elif source["type"] == "dockerhub-tags":
                latest = _latest_dockerhub_tag(source["repo"])
            elif source["type"] == "dockerhub-release-tags":
                latest = _latest_dockerhub_tag(source["repo"], release_tags=True)
        except (KeyError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            latest = None

    strip_prefix = source.get("strip_prefix") if source else None
    if latest and strip_prefix and latest.startswith(strip_prefix):
        latest = latest[len(strip_prefix):]

    latest_version_cache[app_name] = latest
    return latest


def app_description(app_name):
    return APP_CATALOG.get(app_name, {}).get("description", "No description available.")


def app_url(app_name):
    return APP_CATALOG.get(app_name, {}).get("url", "No URL available.")


def configured_version(app_name):
    return APP_CATALOG.get(app_name, {}).get("version", "unknown")
