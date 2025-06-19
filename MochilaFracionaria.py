import sys
import locale

# Configuração para saída UTF-8 (evita problemas com caracteres especiais no terminal)
sys.stdout.reconfigure(encoding='utf-8')

# Tenta configurar o locale para formato de moeda brasileiro (útil se precisar formatar moeda no futuro)
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    print("Erro ao configurar o locale para pt_BR.UTF-8.")

class Item:
    # Classe que representa um item com nome, peso e valor, além do seu valor por unidade de peso (ratio)
    def __init__(self, name, weight, value):
        # name: Nome do item.
        # weight: Peso do item em kg.
        # value: Valor total do item.
        self.name = name
        self.weight = weight
        self.value = value
        self.ratio = value / weight  # Valor por kg (usado para priorizar no algoritmo)

class FractionalKnapsackSolver:
    # Classe responsável por resolver o problema da Mochila Fracionária
    def __init__(self, capacity, items):
        # capacity: Capacidade máxima da mochila (em kg).
        # items: Lista de objetos do tipo Item.
        self.capacity = capacity
        self.items = items
        self.totalValue = 0.0
        self.selectedItems = []
        self.usedCapacity = 0.0  # Para calcular quanto da mochila foi preenchido

    def solve(self):
        # Executa o algoritmo da mochila fracionária.
        # Ordena os itens por valor por kg, seleciona os itens inteiros ou frações que couberem na mochila,
        # acumula o valor total e exibe um resumo detalhado da seleção.

        # Ordena os itens pelo valor por kg (ordem decrescente)
        self.items.sort(key=lambda item: item.ratio, reverse=True)
        remainingCapacity = self.capacity

        print(f"Capacidade total da mochila: {self.capacity} kg\n")

        for item in self.items:
            if remainingCapacity == 0:
                break  # Se a mochila estiver cheia, para o processamento

            if remainingCapacity >= item.weight:
                # Caso o item inteiro caiba na mochila
                remainingCapacity -= item.weight
                self.totalValue += item.value
                self.usedCapacity += item.weight
                self.selectedItems.append((item.name, 1.0, item.value))
                print(f"Adicionou o item completo: {item.name} - {item.weight} kg - R${item.value:.2f}")
            else:
                # Caso só uma fração do item caiba na mochila
                fraction = remainingCapacity / item.weight
                addedValue = item.value * fraction
                self.totalValue += addedValue
                self.usedCapacity += remainingCapacity
                self.selectedItems.append((item.name, fraction, addedValue))
                print(f"Adicionou {fraction * 100:.2f}% do item: {item.name} - {remainingCapacity:.2f} kg - R${addedValue:.2f}")
                remainingCapacity = 0

        self.displaySummary()
        return self.totalValue

    def displaySummary(self):
        # Exibe o resumo final: valor total acumulado e detalhamento de cada item selecionado (inteiro ou parcial)
        print(f"\nValor total final da mochila: R${self.totalValue:.2f}")
        print("\nResumo dos itens selecionados:")
        for name, fraction, value in self.selectedItems:
            itemType = "Item completo" if fraction == 1.0 else f"{fraction * 100:.2f}% do item"
            print(f"- {itemType}: {name} (Valor: R${value:.2f})")

        # Calcula a porcentagem de preenchimento e espaço restante
        filledPercentage = (self.usedCapacity / self.capacity) * 100
        remainingPercentage = 100 - filledPercentage

        print(f"\nA mochila foi preenchida em {filledPercentage:.2f}%")
        print(f"Espaço restante na mochila: {remainingPercentage:.2f}%")

if __name__ == "__main__":
    # Define a capacidade máxima da mochila (em kg)
    backpackCapacity = 16  # kg

    # Lista de itens disponíveis (nome, peso, valor total)
    items = [
        Item("Ouro", 10, 600000),
        Item("Grãos de café", 15, 30000),
        Item("Arroz", 8, 12500),
        Item("Farinha", 20, 10000),
        Item("Açúcar", 7, 8000),
        Item("Petróleo", 19, 150000),
        Item("Cobre", 30, 90000),
        Item("Sal", 22, 5000)
    ]

    solver = FractionalKnapsackSolver(backpackCapacity, items)
    solver.solve()
