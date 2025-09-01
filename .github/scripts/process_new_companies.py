#!/usr/bin/env python3
# %%
import json
import os
import re
from typing import List, Dict
from llm_call import GeminiClient
from pydantic import BaseModel

EVENT_PATH = os.environ.get('GITHUB_EVENT_PATH')
REPO_PATH = os.environ.get('REPO_PATH', '.')
COMPANIES_JSON = os.path.join(REPO_PATH, 'assets', 'data', 'companies.json')
REFERENCES_JSON = os.path.join(REPO_PATH, 'assets', 'data', 'references.json')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

def load_issue_body() -> str:
    if not EVENT_PATH or not os.path.exists(EVENT_PATH):
        return ''
    with open(EVENT_PATH, 'r') as f:
        payload = json.load(f)
    return payload.get('issue', {}).get('body', '')


def load_companies(path: str) -> List[Dict]:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_references(path: str) -> List[str]:
    try:
        with open(path, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_companies(path: str, data: List[Dict]):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write("\n")

def save_references(path: str, data: List[str]):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write("\n")

def normalize_name(s: str) -> str:
    return re.sub(r"\s+", " ", (s or '').strip()).lower()


class CompanyRecord(BaseModel):
    company: str
    status: str
    trajectory: str
    category: str

def format_company_records(
    input_text: str,
    gemini_client: GeminiClient,
    model: str = "gemini-2.5-flash",
)-> list[CompanyRecord]:
    prompt = f"""
        Format the input text into structured json objects.
        Fields:
        - company: the name of the company
        - status: the current status of the company
        - trajectory: a short description of the company's trajectory
        - category: the category of the company (one of: public, private, acquired)
        
        Input text:
        {input_text}
    """
    response = gemini_client.get_response(
        prompt=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': list[CompanyRecord],
        },
        model=model,
        
    )
    return response.parsed


def get_company_records(
    input_text: str,
    gemini_client: GeminiClient,
    model: str = "gemini-2.5-flash",
    )-> tuple[str, list[str]]:
    prompt = f"""
        Extract company records from the input text below and then search the web for more information about the company, such as current status, funding rounds, valuations, acquisitions, etc. 
        
        Return three fields: company, status, trajectory, category (one of: public, private, acquired). Do not include any commentary.
        
        Rules:
        - If a URL is given, infer likely target companies from the URL text (name or domain).
        - Be concise but accurate; one to two short sentences for trajectory/status.
        - If uncertain, include the best-guess company name and category private.
        
        Input text (may be a URL or free text listing companies):
        {input_text}
    """
    
    response = gemini_client.get_response(
        prompt=prompt,
        config={"tools": [{'google_search': {}}]},
        model=model,
    )

    company_records = gemini_client.process_response(
        response,
        add_citations=False,
        as_json=False,
    )

    references = gemini_client.get_cited_sites(response)

    return company_records, references


def call_llm_to_extract(body: str) -> tuple[List[CompanyRecord], List[str]]:
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not configured in repo secrets.")

    raw_company_records, references = get_company_records(
        input_text=body,
        gemini_client=GeminiClient(GOOGLE_API_KEY),
        model="gemini-2.5-flash",
    )

    formatted_company_records = format_company_records(
        input_text=raw_company_records,
        gemini_client=GeminiClient(GOOGLE_API_KEY),
        model="gemini-2.5-flash-lite",
    )
    return formatted_company_records, references


def main():
    out_path = os.environ.get('GITHUB_OUTPUT')
    def set_output(key: str, val: str):
        if out_path:
            with open(out_path, 'a') as f:
                f.write(f"{key}={val}\n")

    try:
        body = load_issue_body()
        existing = load_companies(COMPANIES_JSON)
        existing_references = load_references(REFERENCES_JSON)
        existing_norm = {normalize_name(e.get('company','') \
            if isinstance(e, dict) else e.company) for e in existing}

        llm_items, references = call_llm_to_extract(body)

        added = []
        for it in llm_items:
            name_norm = normalize_name(it.company)
            if name_norm and name_norm not in existing_norm:
                added.append(it)
                existing_norm.add(name_norm)
                existing.append(it.model_dump())

        changed = bool(added)
        if changed:
            save_companies(COMPANIES_JSON, existing)
            save_references(REFERENCES_JSON, existing_references + references)
    
        set_output('changed', 'true' if changed else 'false')
        set_output('added_names', ", ".join([a.company for a in added]))
        set_output('error', '')
        
    except Exception as e:
        # Surface the error but don’t crash the entire job; follow-up steps can comment
        msg = str(e).replace('\n',' ')
        print(f"::error::{msg}")
        set_output('changed', 'false')
        set_output('added_names', '')
        set_output('error', msg)


if __name__ == '__main__':
    main()

