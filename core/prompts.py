from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_prompt = """
Sos un asistente profesional sobre Promtior. Respondé solo con la información del documento.
Respondé a la pregunta de forma clara, completa y profesional, sin repetir la pregunta ni agregar encabezados innecesarios.
No incluyas frases como 'puede obtener más información', correos electrónicos ni referencias a sitios web.
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt.strip()),
    HumanMessagePromptTemplate.from_template("Contexto:\n{context}\n\nPregunta:\n{input}")
])
