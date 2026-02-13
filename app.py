import argparse

from converter import convert_to_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte uma landing page para JSON compatível com Elementor"
    )
    parser.add_argument("source", help="URL (http/https) ou caminho de arquivo HTML local")
    parser.add_argument("--output", default="template.json", help="Arquivo JSON de saída")
    args = parser.parse_args()

    convert_to_json(args.source, args.output)
    print(f"Template gerado em: {args.output}")


if __name__ == "__main__":
    main()
