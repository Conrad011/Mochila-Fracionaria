// Obtive ajuda de uma IA na transcrição do código abaixo. 
// Sua versão inicial foi feita em Python, pois é a linguagem que conheço. 
// Inclusive, disponibilizei o código original em um arquivo neste mesmo repositório.

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Item {
    String name;
    double weight;
    double value;
    double ratio; // valor por kg

    public Item(String name, double weight, double value) {
        this.name = name;
        this.weight = weight;
        this.value = value;
        this.ratio = value / weight;
    }
}

class FractionalKnapsackSolver {
    double capacity;
    List<Item> items;
    double totalValue;
    List<SelectedItem> selectedItems;
    double usedCapacity;

    // Classe auxiliar para armazenar o item selecionado e sua fração
    static class SelectedItem {
        String name;
        double fraction;
        double value;

        public SelectedItem(String name, double fraction, double value) {
            this.name = name;
            this.fraction = fraction;
            this.value = value;
        }
    }

    public FractionalKnapsackSolver(double capacity, List<Item> items) {
        this.capacity = capacity;
        this.items = items;
        this.totalValue = 0.0;
        this.selectedItems = new ArrayList<>();
        this.usedCapacity = 0.0;
    }

    public double solve() {
        // Ordena os itens pelo valor por kg (decrescente)
        items.sort(Comparator.comparingDouble((Item i) -> i.ratio).reversed());

        double remainingCapacity = capacity;
        System.out.printf("Capacidade total da mochila: %.2f kg%n%n", capacity);

        for (Item item : items) {
            if (remainingCapacity == 0) {
                break;
            }

            if (remainingCapacity >= item.weight) {
                // Adiciona o item completo
                remainingCapacity -= item.weight;
                totalValue += item.value;
                usedCapacity += item.weight;
                selectedItems.add(new SelectedItem(item.name, 1.0, item.value));
                System.out.printf("Adicionou o item completo: %s - %.2f kg - R$%.2f%n",
                        item.name, item.weight, item.value);
            } else {
                // Adiciona fração do item
                double fraction = remainingCapacity / item.weight;
                double addedValue = item.value * fraction;
                totalValue += addedValue;
                usedCapacity += remainingCapacity;
                selectedItems.add(new SelectedItem(item.name, fraction, addedValue));
                System.out.printf("Adicionou %.2f%% do item: %s - %.2f kg - R$%.2f%n",
                        fraction * 100, item.name, remainingCapacity, addedValue);
                remainingCapacity = 0;
            }
        }

        displaySummary();
        return totalValue;
    }

    private void displaySummary() {
        System.out.printf("%nValor total final da mochila: R$%.2f%n", totalValue);
        System.out.println("\nResumo dos itens selecionados:");
        for (SelectedItem si : selectedItems) {
            String itemType = si.fraction == 1.0 ? "Item completo" : String.format("%.2f%% do item", si.fraction * 100);
            System.out.printf("- %s: %s (Valor: R$%.2f)%n", itemType, si.name, si.value);
        }

        double filledPercentage = (usedCapacity / capacity) * 100;
        double remainingPercentage = 100 - filledPercentage;

        System.out.printf("%nA mochila foi preenchida em %.2f%%%n", filledPercentage);
        System.out.printf("Espaço restante na mochila: %.2f%%%n", remainingPercentage);
    }
}

public class MochilaFracionaria {
    public static void main(String[] args) {
        double backpackCapacity = 16.0;

        List<Item> items = new ArrayList<>();
        items.add(new Item("Ouro", 10, 600000));
        items.add(new Item("Grãos de café", 15, 30000));
        items.add(new Item("Arroz", 8, 12500));
        items.add(new Item("Farinha", 20, 10000));
        items.add(new Item("Açúcar", 7, 8000));
        items.add(new Item("Petróleo", 19, 150000));
        items.add(new Item("Cobre", 30, 90000));
        items.add(new Item("Sal", 22, 5000));

        FractionalKnapsackSolver solver = new FractionalKnapsackSolver(backpackCapacity, items);
        solver.solve();
    }
}
