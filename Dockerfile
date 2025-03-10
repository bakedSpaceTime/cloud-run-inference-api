FROM ollama/ollama
ENV HOME /root
WORKDIR /
RUN ollama serve & sleep 10 && ollama pull gemma:2b
# RUN ollama serve & sleep 10 && ollama pull deepseek-r1:32b
# RUN ollama serve & sleep 10 && ollama pull phi4
# RUN ollama serve & sleep 10 && ollama pull llama3.1
# RUN ollama serve & sleep 10 && ollama pull qwen2.5-coder:32b
# RUN ollama serve & sleep 10 && ollama pull mistral
# RUN ollama serve & sleep 10 && ollama pull nomic-embed-text
ENTRYPOINT ["ollama","serve"]

