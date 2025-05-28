# Documentación del Chatbot RAG Promtior

## 1. Objetivo de la documentación

En este documento presento cómo abordé el reto de construir un asistente conversacional para Promtior utilizando un enfoque RAG. Aquí detallo la lógica de implementación, los principales desafíos y las tecnologías empleadas para que pueda valorarse la solución propuesta.

## 2. Overview del proyecto

Este proyecto monta un pipeline RAG que usa un PDF como única fuente de conocimiento:

1. Cargo y divido el documento en fragmentos con LangChain.
2. Genero embeddings con MiniLM y los indexo en FAISS.
3. Cuando llega una consulta, recupero los trozos más relevantes, compongo un prompt y lo envío al modelo Mixtral-8x7B vía Together.ai.
4. Finalmente limpio y post-proceso la respuesta antes de devolverla al usuario a través de FastAPI.

## 3. Diagrama de flujo
El flujo es el siguiente:

```mermaid
flowchart TB
    Cliente --> FastAPI
    FastAPI --> ask_question
    ask_question --> decision{¿Es saludo?}
    decision -- Sí --> respuesta_amistosa[Respuesta amistosa]
    decision -- No --> PyPDFLoader
    PyPDFLoader --> TextSplitter
    TextSplitter --> MiniLM_Embeddings
    MiniLM_Embeddings --> FAISS_Index
    FAISS_Index --> Retrieval[Retrieval (chunks)]
    Retrieval --> Prompt_Template
    Prompt_Template --> Invoke_Mixtral[Invoke – Mixtral-8x7B]
    Invoke_Mixtral --> Post_Procesamiento
    Post_Procesamiento --> FastAPI_Devuelve[FastAPI devuelve respuesta]
    FastAPI_Devuelve --> Cliente
```

## 4. Funcionamiento del proyecto

Este chatbot basado en RAG responde preguntas sobre la compañía Promtior tomando su información directamente del PDF.  
Cuando un usuario envía una consulta, el sistema:

1. Divide el PDF en fragmentos mediante LangChain.
2. Genera embeddings con el modelo `all-miniLM` de Hugging Face.
3. Almacena y recupera vectores usando FAISS.
4. Recupera los fragmentos más relevantes y los combina en un prompt.
5. Envía el prompt a un LLM remoto (“Mixtral-8x7B” vía Together.ai).
6. Post-procesa la respuesta: filtra prefijos, saludos y referencias, y la devuelve al usuario.

> **Nota**: Elegí usar el PDF en lugar de scraping de la web para asegurarme de extraer datos precisos como la fecha de fundación y detalles concretos de los servicios.

## 5. Tecnologías usadas

- **Lenguaje y servidor**: Python 3 + FastAPI + Uvicorn
- **Pipeline RAG**: LangChain + FAISS + Embeddings MiniLM
- **Modelo LLM remoto**: Mixtral-8x7B vía Together.ai
- **Despliegue**:
  - **Backend** en AWS EC2 (SSH + `nohup`)
  - **Frontend** en Vercel
- **Frontend**: Next.js + Redux Toolkit + Redux Persist + Tailwind CSS

## 6. Estructura de carpetas del proyecto

/
├─ api/
│ └─ routes/
│ └─ chat.py
├─ core/
│ ├─ embeddings.py
│ ├─ prompts.py
│ └─ rag_chain.py
├─ doc/
│ ├─ promtior.pdf
│ └─ diagrama.png
├─ models/
│ └─ faiss_index/
├─ pages/
│ └─ api/
│ └─ chat.ts
├─ main.py
├─ next.config.js
└─ README.md

## 7. Desafíos encontrados

- **Curva de aprendizaje de Python**: Nunca había usado Python; investigué la arquitectura de carpetas y pedí ayuda a IA para modularizar código.
- **Problemas de inferencia local**: Ollama y Llama 2 tardaban más de un minuto y requerían GPU.
- **Elección de LLM**: Llama 3 generaba respuestas genéricas o con preguntas de seguimiento; finalmente adopté Mixtral-8x7B, que respondió de manera más robusta y precisa.
- **Contexto ambiguo**: Preguntas vagas (“¿qué ofrece?”, “¿cuándo se fundó?”) no resolvían a qué parte del PDF referirse.
- **Scraping vs. PDF**: El scraping devolvía datos erróneos o genéricos; el PDF garantizó obtener detalles exactos (fecha de fundación, servicios clave).

## 8. Links de interés y contacto

- **LinkedIn**: [tu perfil]
- **GitHub**: [tu repositorio]
- **Portfolio**: [tu sitio]
- **Email**: enriquez.jose@gmail.com
- **Demo del bot**: https://chatbot-front-three.vercel.app/
