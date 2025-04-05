import os
from openai import AssistantEventHandler, OpenAI
from dotenv import load_dotenv
from typing_extensions import override
from system_prompt import SYSTEM_PROMPT

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MedicalEventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.response = {"content": "", "citations": []}

    @override
    def on_message_done(self, message) -> None:
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []

        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        self.response = {
            "content": message_content.value,
            "citations": citations
        }

def process_initial_analysis(file_paths):
    try:
        assistant = client.beta.assistants.create(
            name="Medical Report Analyst",
            instructions=SYSTEM_PROMPT,
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        )

        vector_store = client.vector_stores.create(name="Medical Reports")
        file_streams = [open(path, "rb") for path in file_paths]

        client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )

        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
        )

        thread = client.beta.threads.create(messages=[{
            "role": "user",
            "content": "Analyze these medical reports per protocol"
        }])

        event_handler = MedicalEventHandler()

        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=event_handler
        ) as stream:
            stream.until_done()

        return {
            "summary": event_handler.response["content"],
            "citations": event_handler.response["citations"],
            "thread_id": thread.id,
            "assistant_id": assistant.id
        }

    except Exception as e:
        return {"error": str(e)}

def handle_followup(thread_id, assistant_id, question):
    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question
        )

        event_handler = MedicalEventHandler()

        with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=event_handler
        ) as stream:
            stream.until_done()

        return {
            "response": event_handler.response["content"],
            "citations": event_handler.response["citations"]
        }

    except Exception as e:
        return {"error": str(e)}
