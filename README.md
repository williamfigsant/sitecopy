# SiteCopy → Elementor JSON (MVP)

Aplicativo inicial para **copiar o conteúdo principal de uma landing page** e gerar um **JSON compatível com a estrutura de template do Elementor** para importação no WordPress.

> ⚠️ Importante: use apenas em páginas que você tem permissão para reproduzir. Respeite direitos autorais, marcas e termos de uso.

## O que este MVP faz

- Lê HTML de uma URL (`http/https`) ou de arquivo local.
- Extrai blocos comuns de venda:
  - título principal (`h1`, `h2`)
  - textos (`p`)
  - imagens (`img`)
  - botões/links (`a`)
- Converte para uma árvore JSON no formato esperado pelo Elementor (`section > column > widgets`).

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso (CLI)

```bash
python app.py "https://exemplo.com/pagina-de-vendas" --output template.json
```

Também aceita arquivo local:

```bash
python app.py "./pagina.html" --output template.json
```

## Uso (API)

```bash
python api.py
```

POST `/convert`

```json
{
  "source": "https://exemplo.com"
}
```

Resposta:

```json
{
  "template": {"title": "Imported from https://exemplo.com", "content": [...]}
}
```

## Próximos passos para chegar mais perto de plugins como Pensil

1. Crawl multipágina (funil completo).
2. Mapeamento de mais widgets (ícones, vídeos, contadores, depoimentos, FAQ, etc.).
3. Detecção de seções por hierarquia visual/CSS.
4. Extração de estilos para aproximar layout original.
5. Exportador para zip/template completo do Elementor.
6. Interface web com preview antes de exportar.

