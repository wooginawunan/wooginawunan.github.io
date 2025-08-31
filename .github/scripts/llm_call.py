# %%
import json
import re
from google import genai

class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def get_response(
        self, 
        prompt: str, 
        config: genai.types.GenerateContentConfig = None,
        model: str = "gemini-2.5-flash",
        ):
        
        return self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        
    def process_response(
            self,
            response: genai.types.GenerateContentResponse,
            add_citations: bool = False,
            as_json: bool = False,
        ):
        text = response.text
        if as_json:
            if text.startswith('```json'):
                json_match = re.search(
                    r'```json\s*(.*?)\s*```', text,re.DOTALL)
                if json_match:
                    json_text = json_match.group(1)
                    json_response = json.loads(json_text)
                    return json_response
                else:
                    print("No JSON found in response")
                    return None

        elif add_citations:
            return self.add_citations(response)
        else:
            return text

    def get_cited_sites(
            self, response: genai.types.GenerateContentResponse
        )-> list[str]:
        return [
            site.web.uri for site in response.candidates[0].grounding_metadata.grounding_chunks
        ]
    
    def get_search_query(self, 
            response: genai.types.GenerateContentResponse
        )-> list[str]:
        return response.candidates[0].grounding_metadata.web_search_queries
                
    def add_citations(
            self, response: genai.types.GenerateContentResponse
        )-> str:
        
        text = response.text
        supports = response.candidates[0].grounding_metadata.grounding_supports
        chunks = response.candidates[0].grounding_metadata.grounding_chunks

        # Sort supports by end_index in descending order to avoid shifting issues when inserting.
        sorted_supports = sorted(
            supports, key=lambda s: s.segment.end_index, reverse=True
        )

        for support in sorted_supports:
            end_index = support.segment.end_index
            if support.grounding_chunk_indices:
                # Create citation string like [1](link1)[2](link2)
                citation_links = []
                for i in support.grounding_chunk_indices:
                    if i < len(chunks):
                        uri = chunks[i].web.uri
                        citation_links.append(f"[{i + 1}]({uri})")

                citation_string = ", ".join(citation_links)
                text = text[:end_index] + citation_string + text[end_index:]

        return text