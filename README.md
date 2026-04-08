#  TCG Proxy Card Printer

> Gera folhas PDF prontas para impressão com suas proxies tipo Magic: The Gathering — feito pela comunidade, para a comunidade.

---

##  O que é isso?

Uma ferramenta de linha de comando simples que recebe a imagem de uma carta (criada por ferramentas como [TCG Card Builder](https://mtgcardbuilder.com)) e organiza múltiplas cópias em uma folha A4 ou Letter, pronta para imprimir e cortar.

**Resultado:** folha 3×3 com marcas de corte, em PDF de alta qualidade.

---

##  Pré-requisitos

- Python **3.11+**
- pip

---

##  Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Rafafelbrown/TCG-Proxy-Card-Printer.git
cd mtg-proxy-printer

# 2. (Recomendado) Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

---

##  Uso

```bash
python card_printer.py <caminho_da_imagem> [opções]
```

### Exemplos rápidos

```bash
# Básico — 9 cópias em folha A4
python card_printer.py minha_carta.png

# 18 cópias (2 páginas)
python card_printer.py carta.jpg --copies 18

# Papel carta (US Letter)
python card_printer.py carta.png --paper LETTER

# Sem marcas de corte
python card_printer.py carta.png --no-cut-marks

# Bordas menores para aproveitar mais espaço
python card_printer.py carta.png --margin 5 --gap 1

# Salvar com nome personalizado
python card_printer.py carta.png --output meu_deck_proxy.pdf
```

---

##  Opções

| Opção | Padrão | Descrição |
|---|---|---|
| `image` | *(obrigatório)* | Caminho para a imagem da carta (PNG, JPG, etc.) |
| `--copies N` | `9` | Total de cópias a imprimir |
| `--cols N` | `3` | Número de colunas por página |
| `--rows N` | `3` | Número de linhas por página |
| `--output FILE` | `proxy_sheet.pdf` | Nome do arquivo PDF gerado |
| `--paper SIZE` | `A4` | Tamanho do papel: `A4` ou `LETTER` |
| `--margin MM` | `10` | Margem da página em milímetros |
| `--gap MM` | `2` | Espaço entre as cartas em milímetros |
| `--no-cut-marks` | *(ativo)* | Desativa as marcas de corte nos cantos |

---

##  Dicas de Impressão

1. **Escala:** Imprima sempre em **100% / tamanho real** — nunca "ajustar à página"
2. **Papel:** Papel **couché** ou **fotográfico** matte dá um acabamento profissional
3. **Corte:** Use as **marcas de corte cinzas** nos cantos como guia para tesoura ou guilhotina
4. **Sleeve:** Cartas proxy ficam ótimas dentro de sleeve com um basic land embaixo

---

##  Estrutura do Projeto

```
mtg-proxy-printer/
├── card_printer.py     # Script principal
├── requirements.txt    # Dependências Python
├── README.md           # Este arquivo
└── examples/           # Imagens de exemplo (opcional)
```

---

##  requirements.txt

```
Pillow>=10.0.0
reportlab>=4.0.0
```

---

##  Contribuindo

Pull requests são bem-vindos! Algumas ideias para contribuições:

- Suporte a múltiplas imagens diferentes na mesma folha
- Interface gráfica (GUI) com Tkinter ou web com Gradio
- Suporte a frente e verso (double-faced cards)
- Preset de tamanho exato de carta TCG (63mm × 88mm)
- Exportar também como PNG de alta resolução

Para contribuir:

```bash
# Fork o repositório, crie um branch e abra um PR
git checkout -b feature/minha-feature
git commit -m "feat: minha nova funcionalidade"
git push origin feature/minha-feature
```

---

##  Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para mais informações.

---

> **Aviso Legal:** Este projeto é destinado exclusivamente ao uso pessoal e educacional. Não use proxies em torneios oficiais.
