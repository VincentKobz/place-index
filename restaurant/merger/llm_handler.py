import json
from dataclasses import dataclass
from typing import List

from openai import OpenAI, AuthenticationError, APIConnectionError

from restaurant import LLM_KEY


@dataclass
class ExpectedAnswer:
    tags: List[str]


class LLMHandler:
    def __init__(self):
        self.client = OpenAI(base_url="https://api.deepseek.com", api_key=LLM_KEY)
        self.merge_tags_prompt = """
        I will provide you with two lists of tags from different sources. These tags describe the type of cuisine or food offered by a restaurant.
        Your task is to merge these lists into a single, cohesive list by selecting the most appropriate tags while avoiding redundancies or duplicates.
        Ensure that the final list is coherent and accurately represents the style of cuisine or type of restaurant.
        The names of the tags should be uniform, starting with a capital letter and using spaces where necessary.
        You should remove "point of interest" and "establishment", "restaurant" and "food" from the tags:
        exemple: "Italian restaurant" -> "Italian"

        Expected OUTPUT JSON object: {tags: List[str]}
        """

        self.model = "deepseek-chat"

    def merge_tags(self, tags_1: List[str], tags_2: List[str]) -> List[str]:
        """
        Merge two lists of tags using the LLM
        @param tags_1:
        @param tags_2:
        @return:
        """
        try:
            llm_answer = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.merge_tags_prompt},
                    {
                        "role": "user",
                        "content": "List 1: "
                        + " ".join(tags_1)
                        + "\nList 2: "
                        + " ".join(tags_2),
                    },
                ],
                response_format={"type": "json_object"},
            )
        except AuthenticationError as e:
            raise Exception("Invalid LLM API key provided.", e)
        except APIConnectionError as e:
            raise Exception("Error connecting to the LLM API.", e)

        json_content = json.loads(llm_answer.choices[0].message.content)
        return ExpectedAnswer(**json_content).tags
