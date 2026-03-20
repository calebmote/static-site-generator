from textnode import TextNode, textType

def main():
    node = TextNode("This is some anchor text", textType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()