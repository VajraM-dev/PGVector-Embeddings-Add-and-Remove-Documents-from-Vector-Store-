import os
from langchain_aws import ChatBedrock
from langchain_aws.embeddings.bedrock import BedrockEmbeddings
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(".env.dev"))

LLM_MODEL_ID = os.environ.get("LLM_MODEL_ID")
EMBEDDING_MODEL_ID = os.environ.get("EMBEDDING_MODEL_ID")
MODEL_TEMPERATURE = os.environ.get("MODEL_TEMPERATURE")
MODEL_REGION_NAME = os.environ.get("MODEL_REGION_NAME")
MODEL_CRED_PROFILE_NAME = os.environ.get("MODEL_CRED_PROFILE_NAME")
MODEL_GUARDRAIL = os.environ.get("MODEL_GUARDRAIL")
MODEL_GUARDRAIL_VERSION = os.environ.get("MODEL_GUARDRAIL_VERSION")

embedding_model = BedrockEmbeddings(model_id=EMBEDDING_MODEL_ID, 
                  region_name=MODEL_REGION_NAME, 
                  credentials_profile_name=MODEL_CRED_PROFILE_NAME
                )

guardrails={"guardrailIdentifier": MODEL_GUARDRAIL, "guardrailVersion": MODEL_GUARDRAIL_VERSION, "trace": True}

llm = ChatBedrock(model_id=LLM_MODEL_ID, 
                  model_kwargs={"temperature": float(MODEL_TEMPERATURE)}, 
                  region_name=MODEL_REGION_NAME, 
                  credentials_profile_name=MODEL_CRED_PROFILE_NAME, 
                  guardrails=guardrails
                )