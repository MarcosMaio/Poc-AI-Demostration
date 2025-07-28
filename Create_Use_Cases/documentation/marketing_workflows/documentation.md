# Marketing Agents – API Reference

This document details each workflow available in the **Marketing Agents** package, the JSON payload you must send to trigger it, and the structure of the data you’ll receive back.  Use it to wire Postman collections, front‑end calls, or other integrations.

---

## 1 · Workflows & End‑points

| ID    | Workflow         | Business Goal                                              | End‑point (POST)                                | Pipeline (agents in order)                                            |
| ----- | ---------------- | ---------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------- |
| **1** | **Campaign‑30d** | Produce a 30‑day multi‑channel content strategy & calendar | `http://localhost:8000/studio/workflows/1/run/` | `ContentStrategistAgent → PostPlannerAgent → ComplianceReviewerAgent` |
| **2** | **Single‑Post**  | Generate the full copy for one post, then sanitise it      | `http://localhost:8000/studio/workflows/2/run/` | `PostContentCreatorAgent → PostContentComplianceAgent`                |
| **3** | **Doc‑Health**   | Compute quality metrics & a health score for any document  | `http://localhost:8000/studio/workflows/3/run/` | `DocumentHealthAnalyzerAgent → DocumentHealthComplianceAgent`         |
| **4** | **Brand Brief**  | Extract a structured brand brief from a website URL        | `http://localhost:8000/studio/workflows/4/run/` | `WebsiteBrandBriefAgent → BrandBriefComplianceAgent`                  |

> **Tip** All requests are **POST** with a JSON body under the key `inputs`:
>
> ```json
> { "inputs": { … } }
> ```
>
> You don’t need to send `agent_keys` – every workflow is already wired server‑side.

---

## 2 · Payloads

Below you’ll find the *exact* input keys expected by each workflow (English snake‑case), an example request body, and a sketch of the output returned.

### 2.1 Campaign‑30d  — `/studio/workflows/1/run/`

| **Input key**  | **Type**      | **Description**                                                     |
| -------------- | ------------- | ------------------------------------------------------------------- |
| `subject`      | string        | High‑level umbrella topic for the campaign.                         |
| `objective`    | string        | Communication objective ("Engagement", "Lead Gen" …).               |
| `language`     | string        | Language code or name – the whole pipeline writes in this language. |
| `platforms`    | array<string> | Allowed channels e.g. `["linkedin","instagram","blog"]`.            |
| `brand`        | object        | Optional brand guidelines / tone rules. Empty `{}` if none.         |
| `current_date` | ISO date      | Today’s date so the planner can start **tomorrow**.                 |

**Sample Request**

```bash
POST /studio/workflows/1/run/
Content‑Type: application/json

{
  "inputs": {
    "subject": "Agentes de IA e como eles estão mudando o mundo.",
    "objective": "Engajamento",
    "language": "Portuguese",
    "platforms": ["linkedin", "instagram", "blog"],
    "brand": {},
    "current_date": "2025-07-01"
  }
}
```

**Output**
A nested JSON with three logical parts:

1. **Strategy brief** – plain‑text string returned by *ContentStrategistAgent*.
2. **planned\_posts** – JSON array of 30 post ideas (from *PostPlannerAgent*).
3. **sanitised\_posts** – final compliant array (from *ComplianceReviewerAgent*).

> The API packs those three pieces into one JSON document under intuitive keys (`strategy`, `planned_posts`, `posts`).

---

### 2.2 Single‑Post  — `/studio/workflows/2/run/`

| **Input key**         | **Type**      | **Required** | **Description**                                |
| --------------------- | ------------- | ------------ | ---------------------------------------------- |
| `topic`               | string        | ✓            | Post headline / focus.                         |
| `platform`            | string        | ✓            | One of: `blog`, `linkedin`, `instagram`, etc.  |
| `description`         | string        | ✓            | Brief background / pain‑agitate‑solution text. |
| `keywords`            | array<string> | ✓            | Exactly seven mandatory keywords to weave in.  |
| `audience`            | string        | ✓            | Target segment.                                |
| `custom_instructions` | string        | —            | Extra tone or style notes (optional).          |

**Sample Request**

```json
{
  "inputs": {
    "topic": "Agentes de IA: O Guia Definitivo Para Aumentar a Sua Produtividade",
    "platform": "blog",
    "description": "Bem‑vindo à nova era da produtividade…",
    "keywords": [
      "agentes de ia",
      "inteligência artificial",
      "produtividade no trabalho",
      "automação inteligente",
      "futuro do trabalho",
      "tecnologia e carreira",
      "aumento de capacidade"
    ],
    "audience": "Profissionais curiosos sobre tecnologia e inovação",
    "custom_instructions": ""
  }
}
```

**Output**

```json
{
  "post_text": "<Final compliant post in Markdown or plain text>"
}
```

---

### 2.3 Doc‑Health  — `/studio/workflows/3/run/`

| **Input key**        | **Type** | **Description**                      |
| -------------------- | -------- | ------------------------------------ |
| `content_to_analyze` | string   | Raw Markdown or plain‑text document. |

**Sample Request (truncated)**

```json
{
  "inputs": {
    "content_to_analyze": "# Agentes de IA: O Guia Definitivo …"
  }
}
```

**Output** – validated metrics JSON

```json
{
  "words": 2745,
  "sentences": 119,
  "paragraphs": 56,
  "headings": 14,
  "reading_time_minutes": 11,
  "scores": {
    "correctness": 90,
    "vocabulary": 80,
    "readability": 70,
    "accessibility": 70,
    "styles": 80,
    "terms": 80,
    "sentence_structure": 70
  },
  "content_score": 77
}
```

---

### 2.4 Brand Brief  — `/studio/workflows/4/run/`

| **Input key** | **Type** | **Description**                   |
| ------------- | -------- | --------------------------------- |
| `website_url` | string   | Absolute URL of the company site. |

**Sample Request**

```json
{
  "inputs": {
    "website_url": "https://www.marica.rj.gov.br/"
  }
}
```

**Output** – clean brand brief JSON

```json
{
  "brand_name": "Prefeitura de Maricá",
  "brand_description": "Responsável por políticas públicas…",
  "core_messaging": "Inclusão social & desenvolvimento…",
  "audience": ["Cidadãos de Maricá", "Visitantes"],
  "value_proposition": "Serviços públicos de qualidade…",
  "tone_of_voice": ["Informativo", "Comunitário"],
  "industry": ["Setor Público"],
  "keywords_and_themes": ["Transporte público", "Renda básica", "Educação"],
  "topics": ["Programas sociais", "Mobilidade urbana", "Educação"]
}
```

---

## 3 · Error Handling

* **400 Bad Request** – missing or malformed `inputs` key.
* **422 Unprocessable Entity** – one or more required fields missing / invalid type.
* **500 Internal Server Error** – unhandled failure in agent pipeline (check logs).

