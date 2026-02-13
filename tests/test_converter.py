import unittest

from converter import build_elementor_template, extract_nodes


class ConverterTests(unittest.TestCase):
    def test_extract_nodes_and_build_template(self):
        html = """
        <html><body>
          <h1>Oferta Imperdível</h1>
          <p>Compre agora e ganhe bônus.</p>
          <img src="https://cdn.exemplo.com/hero.jpg" />
          <a href="https://checkout.exemplo.com">Quero comprar</a>
        </body></html>
        """

        nodes = extract_nodes(html)
        self.assertEqual(len(nodes), 4)

        template = build_elementor_template(nodes, "teste")
        widgets = template["content"][0]["elements"][0]["elements"]

        self.assertEqual(template["title"], "Imported from teste")
        self.assertEqual(
            [w["widgetType"] for w in widgets],
            ["heading", "text-editor", "image", "button"],
        )


if __name__ == "__main__":
    unittest.main()
