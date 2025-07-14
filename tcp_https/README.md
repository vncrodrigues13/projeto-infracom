# Sistema de Quiz HTTPS

Este diretório contém uma implementação do sistema de quiz usando comunicação segura via HTTPS (SSL/TLS).

## Arquivos

- `servidor_https.py` - Servidor HTTPS que gerencia o quiz
- `clientes_https.py` - Clientes que se conectam ao servidor HTTPS
- `start.py` - Script para executar automaticamente servidor e clientes
- `README.md` - Este arquivo

## Funcionalidades

- **Comunicação Segura**: Usa SSL/TLS para criptografar toda a comunicação
- **Certificado Auto-assinado**: Gera automaticamente certificados SSL
- **Múltiplos Clientes**: Suporta até 16 clientes simultâneos
- **Quiz Interativo**: 10 perguntas com 4 opções cada
- **Sistema de Pontuação**: Pontuação decrescente por resposta correta

## Como Executar

### Opção 1: Execução Automática
```bash
python3 start.py
```

### Opção 2: Execução Manual

1. **Iniciar o servidor**:
```bash
python3 servidor_https.py
```

2. **Em outro terminal, executar os clientes**:
```bash
python3 clientes_https.py
```

## Requisitos

- Python 3.6+
- OpenSSL (para gerar certificados)
- Módulos Python: `socket`, `threading`, `ssl`, `random`, `time`

## Certificados SSL

O sistema gera automaticamente certificados SSL auto-assinados:
- `server.crt` - Certificado do servidor
- `server.key` - Chave privada do servidor

**Nota**: Como são certificados auto-assinados, os clientes ignoram a verificação de certificado para fins de demonstração.

## Porta Padrão

- **Porta**: 12345
- **Host**: 127.0.0.1 (localhost)

## Estrutura do Quiz

1. Cada cliente recebe 5 perguntas aleatórias
2. Perguntas têm 4 opções (A, B, C, D)
3. Pontuação decresce a cada resposta correta
4. Resultado final mostra ranking dos clientes

## Segurança

- Comunicação criptografada via TLS 1.2+
- Certificados RSA 4096 bits
- Conexões seguras entre cliente e servidor

## Diferenças do TCP Simples

- **Criptografia**: Toda comunicação é criptografada
- **Autenticação**: Verificação de certificados SSL
- **Integridade**: Proteção contra interceptação de dados
- **Confidencialidade**: Dados não podem ser lidos por terceiros 