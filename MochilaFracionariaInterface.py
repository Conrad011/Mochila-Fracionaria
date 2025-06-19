

import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import locale

# Configurar locale para moeda brasileira
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Linux
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')  # Windows

def formatarMoeda(valor):
    return locale.currency(valor, grouping=True)

class Item:
    def __init__(self, nome, peso, valor):
        self.nome = nome
        self.peso = peso
        self.valor = valor
        self.ratio = valor / peso

class FractionalKnapsackApp:
    def __init__(self, root):
        self.itens = [
            Item("Ouro", 10, 600000),
            Item("Grãos de café", 15, 30000),
            Item("Arroz", 8, 12500),
            Item("Farinha", 20, 10000),
            Item("Açúcar", 7, 8000),
            Item("Petróleo", 19, 150000),
            Item("Cobre", 30, 90000),
            Item("Sal", 22, 5000)
        ]
        self.varCheckboxes = []
        self.checkboxWidgets = []
        self.root = root
        self.root.title("Calculadora da Mochila Fracionária - Adicionar/Remover Itens")
        self.root.configure(bg="#f0f0f0")
        self.fontPadrao = ("Arial", 12)
        self.createInterface()

    def createInterface(self):
        frameCadastro = tk.LabelFrame(self.root, text="Adicionar Novo Item", font=self.fontPadrao, bg="#f0f0f0")
        frameCadastro.pack(padx=10, pady=10, fill="x")

        tk.Label(frameCadastro, text="Nome:", font=self.fontPadrao, bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.entryNome = tk.Entry(frameCadastro, font=self.fontPadrao)
        self.entryNome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frameCadastro, text="Peso (kg):", font=self.fontPadrao, bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.entryPeso = tk.Entry(frameCadastro, font=self.fontPadrao)
        self.entryPeso.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frameCadastro, text="Valor (R$):", font=self.fontPadrao, bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        self.entryValor = tk.Entry(frameCadastro, font=self.fontPadrao)
        self.entryValor.grid(row=2, column=1, padx=5, pady=5)

        btnAdicionar = tk.Button(frameCadastro, text="Adicionar Item", command=self.addItem, font=self.fontPadrao, bg="#2196F3", fg="white")
        btnAdicionar.grid(row=3, columnspan=2, pady=10)

        self.frameCheckbox = tk.LabelFrame(self.root, text="Selecione os Itens", font=self.fontPadrao, bg="#f0f0f0")
        self.frameCheckbox.pack(padx=10, pady=10, fill="x")

        for item in self.itens:
            var = tk.IntVar(value=1)
            cb = tk.Checkbutton(self.frameCheckbox,
                                text=f"{item.nome} - Peso: {item.peso} kg - Valor: {formatarMoeda(item.valor)}",
                                variable=var, font=self.fontPadrao, bg="#f0f0f0")
            cb.pack(anchor='w')
            self.varCheckboxes.append(var)
            self.checkboxWidgets.append(cb)

        frameBotoesSelecao = tk.Frame(self.root, bg="#f0f0f0")
        frameBotoesSelecao.pack(pady=5)

        btnSelecionarTodos = tk.Button(frameBotoesSelecao, text="Selecionar Todos", command=self.selectAll,
                                       font=self.fontPadrao, bg="#FF9800", fg="white", padx=10, pady=5)
        btnSelecionarTodos.pack(side='left', padx=5)

        btnDesmarcarTodos = tk.Button(frameBotoesSelecao, text="Desmarcar Todos", command=self.deselectAll,
                                      font=self.fontPadrao, bg="#9E9E9E", fg="white", padx=10, pady=5)
        btnDesmarcarTodos.pack(side='left', padx=5)

        btnRemover = tk.Button(self.root, text="Remover Itens Selecionados", command=self.removeItems,
                               font=self.fontPadrao, bg="#f44336", fg="white", padx=10, pady=5)
        btnRemover.pack(pady=5)

        frameCapacidade = tk.Frame(self.root, bg="#f0f0f0")
        frameCapacidade.pack(pady=5)

        tk.Label(frameCapacidade, text="Capacidade da Mochila (kg):", font=self.fontPadrao, bg="#f0f0f0").pack(side='left')
        self.entryCapacidade = tk.Entry(frameCapacidade, font=self.fontPadrao, width=10)
        self.entryCapacidade.pack(side='left', padx=5)

        btnCalcular = tk.Button(self.root, text="Calcular", command=self.calculate,
                                font=self.fontPadrao, bg="#4CAF50", fg="white", padx=10, pady=5)
        btnCalcular.pack(pady=10)

        outputFrame = tk.Frame(self.root)
        outputFrame.pack(pady=5)

        self.output = scrolledtext.ScrolledText(outputFrame, height=15, width=60, font=self.fontPadrao)
        self.output.pack()

    def addItem(self):
        try:
            nome = self.entryNome.get()
            peso = float(self.entryPeso.get())
            valor = float(self.entryValor.get())

            if nome == "" or peso <= 0 or valor <= 0:
                messagebox.showerror("Erro", "Preencha todos os campos com valores válidos!")
                return

            if peso > 1_000_000_000_000 or valor > 1_000_000_000_000:
                messagebox.showerror("Erro", "Peso e Valor não podem ultrapassar 1 trilhão!")
                return

            novoItem = Item(nome, peso, valor)
            self.itens.append(novoItem)

            var = tk.IntVar(value=1)
            cb = tk.Checkbutton(self.frameCheckbox,
                                text=f"{novoItem.nome} - Peso: {novoItem.peso} kg - Valor: {formatarMoeda(novoItem.valor)}",
                                variable=var, font=self.fontPadrao, bg="#f0f0f0")
            cb.pack(anchor='w')
            self.varCheckboxes.append(var)
            self.checkboxWidgets.append(cb)

            self.entryNome.delete(0, tk.END)
            self.entryPeso.delete(0, tk.END)
            self.entryValor.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Erro", "Peso e Valor devem ser números válidos!")

    def removeItems(self):
        indicesParaRemover = [i for i, var in enumerate(self.varCheckboxes) if var.get() == 1]

        if not indicesParaRemover:
            messagebox.showinfo("Aviso", "Selecione pelo menos um item para remover.")
            return

        for index in reversed(indicesParaRemover):
            self.itens.pop(index)
            self.varCheckboxes.pop(index)
            widget = self.checkboxWidgets.pop(index)
            widget.destroy()

    def selectAll(self):
        for var in self.varCheckboxes:
            var.set(1)

    def deselectAll(self):
        for var in self.varCheckboxes:
            var.set(0)

    def fractionalKnapsack(self, capacidade, itensSelecionados):
        itensSelecionados.sort(key=lambda item: item.ratio, reverse=True)

        valorTotal = 0.0
        capacidadeRestante = capacidade
        resultado = []

        for item in itensSelecionados:
            if capacidadeRestante == 0:
                break

            if capacidadeRestante >= item.peso:
                capacidadeRestante -= item.peso
                valorTotal += item.valor
                resultado.append(f"Item completo: {item.nome} - {item.peso} kg - {formatarMoeda(item.valor)}")
            else:
                fracao = capacidadeRestante / item.peso
                valorAdicionado = item.valor * fracao
                valorTotal += valorAdicionado
                resultado.append(f"{fracao*100:.2f}% do item: {item.nome} - {capacidadeRestante:.2f} kg - {formatarMoeda(valorAdicionado)}")
                capacidadeRestante = 0

        resultado.append(f"\nValor total da mochila: {formatarMoeda(valorTotal)}")

        espacoUsado = capacidade - capacidadeRestante
        percentualUsado = (espacoUsado / capacidade) * 100 if capacidade > 0 else 0
        percentualRestante = (capacidadeRestante / capacidade) * 100 if capacidade > 0 else 0

        resultado.append(f"\nA mochila foi preenchida em {percentualUsado:.2f}% (equivalente a {espacoUsado:.2f} kg).")
        resultado.append(f"Ainda restam {capacidadeRestante:.2f} kg de espaço livre na mochila (equivalente a {percentualRestante:.2f}%).")

        return resultado

    def calculate(self):
        try:
            capacidade = float(self.entryCapacidade.get())
            selecionados = [self.itens[i] for i in range(len(self.itens)) if self.varCheckboxes[i].get()]

            if not selecionados:
                messagebox.showwarning("Aviso", "Selecione pelo menos um item!")
                return

            resultado = self.fractionalKnapsack(capacidade, selecionados)

            self.output.delete('1.0', tk.END)
            for linha in resultado:
                self.output.insert(tk.END, linha + "\n")

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido para a capacidade.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FractionalKnapsackApp(root)
    root.mainloop()
