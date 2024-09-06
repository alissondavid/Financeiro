import tkinter as tk
from tkinter import messagebox
import json
import os

class InputDialog(tk.Toplevel):
    def __init__(self, parent, title, label, initial_value='', is_float=True):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.is_float = is_float

        self.geometry("300x150")
        self.resizable(False, False)

        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text=label).pack(pady=10)
        self.entry = tk.Entry(frame)
        self.entry.insert(0, initial_value)
        self.entry.pack(pady=10)
        self.entry.focus_set()

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="OK", command=self.ok).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancelar", command=self.cancel).pack(side=tk.RIGHT, padx=5)

        self.grab_set()
        self.wait_window(self)

    def ok(self):
        value = self.entry.get()
        if self.is_float:
            try:
                float(value)
                self.result = value
                self.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido. Deve ser um número.")
        else:
            if value.strip():
                self.result = value
                self.destroy()
            else:
                messagebox.showerror("Erro", "Descrição não pode ser vazia.")

    def cancel(self):
        self.result = None
        self.destroy()

class FinanceiroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle Financeiro")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.despesas = []
        self.receitas = []

        self.selected_despesa_index = None
        self.selected_receita_index = None

        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Frame para despesas, resumo e receitas
        frame_despesas = tk.Frame(main_frame)
        frame_despesas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        frame_resumo = tk.Frame(main_frame)
        frame_resumo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        frame_receitas = tk.Frame(main_frame)
        frame_receitas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Listbox e botões para despesas
        tk.Label(frame_despesas, text="Despesas", font=("Arial", 14)).pack(pady=5)
        self.despesas_listbox = tk.Listbox(frame_despesas, width=40, height=15)
        self.despesas_listbox.pack(expand=True, fill=tk.BOTH)
        self.despesas_listbox.bind("<<ListboxSelect>>", self.on_despesa_select)

        tk.Button(frame_despesas, text="Adicionar Despesa", command=self.cadastrar_despesa, width=20).pack(pady=5)

        # Botões de editar e excluir despesa
        button_frame = tk.Frame(frame_despesas)
        button_frame.pack(pady=5)

        self.editar_despesa_button = tk.Button(button_frame, text="Editar", command=self.editar_despesa, width=10)
        self.editar_despesa_button.pack(side=tk.LEFT, padx=2)

        self.excluir_despesa_button = tk.Button(button_frame, text="Excluir", command=self.excluir_despesa, width=10)
        self.excluir_despesa_button.pack(side=tk.LEFT)

        # Listbox e botões para receitas
        tk.Label(frame_receitas, text="Receitas", font=("Arial", 14)).pack(pady=5)
        self.receitas_listbox = tk.Listbox(frame_receitas, width=40, height=15)
        self.receitas_listbox.pack(expand=True, fill=tk.BOTH)
        self.receitas_listbox.bind("<<ListboxSelect>>", self.on_receita_select)

        tk.Button(frame_receitas, text="Adicionar Receita", command=self.cadastrar_receita, width=20).pack(pady=5)

        # Botões de editar e excluir receita
        button_frame = tk.Frame(frame_receitas)
        button_frame.pack(pady=5)

        self.editar_receita_button = tk.Button(button_frame, text="Editar", command=self.editar_receita, width=10)
        self.editar_receita_button.pack(side=tk.LEFT, padx=2)

        self.excluir_receita_button = tk.Button(button_frame, text="Excluir", command=self.excluir_receita, width=10)
        self.excluir_receita_button.pack(side=tk.LEFT)

        # Botão para mostrar resumo
        tk.Button(frame_resumo, text="Mostrar Resumo", command=self.mostrar_resumo, width=20).pack(pady=10)

        # Inicializa as listas
        self.update_listboxes()

    def cadastrar_despesa(self):
        descricao_dialog = InputDialog(self.root, "Descrição da Despesa", "Descrição da despesa:", is_float=False)
        descricao = descricao_dialog.result
        if descricao:
            valor_dialog = InputDialog(self.root, "Valor da Despesa", "Valor da despesa:", is_float=True)
            valor = valor_dialog.result
            if valor:
                self.despesas.append((descricao, float(valor)))
                self.update_listboxes()
                self.save_data()
                messagebox.showinfo("Sucesso", "Despesa cadastrada com sucesso!")

    def cadastrar_receita(self):
        descricao_dialog = InputDialog(self.root, "Descrição da Receita", "Descrição da receita:", is_float=False)
        descricao = descricao_dialog.result
        if descricao:
            valor_dialog = InputDialog(self.root, "Valor da Receita", "Valor da receita:", is_float=True)
            valor = valor_dialog.result
            if valor:
                self.receitas.append((descricao, float(valor)))
                self.update_listboxes()
                self.save_data()
                messagebox.showinfo("Sucesso", "Receita cadastrada com sucesso!")

    def editar_despesa(self):
        if self.selected_despesa_index is not None:
            descricao_atual, valor_atual = self.despesas[self.selected_despesa_index]
            descricao_dialog = InputDialog(self.root, "Editar Descrição", "Nova descrição:", descricao_atual, is_float=False)
            nova_descricao = descricao_dialog.result
            if nova_descricao:
                valor_dialog = InputDialog(self.root, "Editar Valor", "Novo valor:", str(valor_atual), is_float=True)
                novo_valor = valor_dialog.result
                if novo_valor:
                    self.despesas[self.selected_despesa_index] = (nova_descricao, float(novo_valor))
                    self.update_listboxes()
                    self.save_data()

    def editar_receita(self):
        if self.selected_receita_index is not None:
            descricao_atual, valor_atual = self.receitas[self.selected_receita_index]
            descricao_dialog = InputDialog(self.root, "Editar Descrição", "Nova descrição:", descricao_atual, is_float=False)
            nova_descricao = descricao_dialog.result
            if nova_descricao:
                valor_dialog = InputDialog(self.root, "Editar Valor", "Novo valor:", str(valor_atual), is_float=True)
                novo_valor = valor_dialog.result
                if novo_valor:
                    self.receitas[self.selected_receita_index] = (nova_descricao, float(novo_valor))
                    self.update_listboxes()
                    self.save_data()

    def excluir_despesa(self):
        if self.selected_despesa_index is not None:
            del self.despesas[self.selected_despesa_index]
            self.update_listboxes()
            self.save_data()

    def excluir_receita(self):
        if self.selected_receita_index is not None:
            del self.receitas[self.selected_receita_index]
            self.update_listboxes()
            self.save_data()

    def mostrar_resumo(self):
        total_despesas = sum(valor for _, valor in self.despesas)
        total_receita = sum(valor for _, valor in self.receitas)

        resumo_window = tk.Toplevel(self.root)
        resumo_window.title("Resumo Financeiro")
        resumo_window.geometry("400x300")

        resumo_frame = tk.Frame(resumo_window)
        resumo_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        tk.Label(resumo_frame, text="Resumo Financeiro", font=("Arial", 16)).pack(pady=10)

        tk.Label(resumo_frame, text=f"Total de Despesas: R$ {total_despesas:.2f}", font=("Arial", 14)).pack(pady=5)
        tk.Label(resumo_frame, text=f"Total de Receitas: R$ {total_receita:.2f}", font=("Arial", 14)).pack(pady=5)

        saldo = total_receita - total_despesas
        saldo_text = f"Saldo: R$ {saldo:.2f}"
        tk.Label(resumo_frame, text=saldo_text, font=("Arial", 14)).pack(pady=5)

        if total_receita > 0:
            percentuais = {
                'Despesas Essenciais (50%)': 0.50 * total_receita,
                'Despesas Variáveis (30%)': 0.30 * total_receita,
                'Poupança (20%)': 0.20 * total_receita
            }
            for descricao, valor in percentuais.items():
                tk.Label(resumo_frame, text=f"{descricao}: R$ {valor:.2f}", font=("Arial", 12)).pack(pady=5)

    def on_despesa_select(self, event):
        selection = self.despesas_listbox.curselection()
        if selection:
            self.selected_despesa_index = selection[0]
            self.editar_despesa_button.config(state=tk.NORMAL)
            self.excluir_despesa_button.config(state=tk.NORMAL)
        else:
            self.selected_despesa_index = None
            self.editar_despesa_button.config(state=tk.DISABLED)
            self.excluir_despesa_button.config(state=tk.DISABLED)

    def on_receita_select(self, event):
        selection = self.receitas_listbox.curselection()
        if selection:
            self.selected_receita_index = selection[0]
            self.editar_receita_button.config(state=tk.NORMAL)
            self.excluir_receita_button.config(state=tk.NORMAL)
        else:
            self.selected_receita_index = None
            self.editar_receita_button.config(state=tk.DISABLED)
            self.excluir_receita_button.config(state=tk.DISABLED)

    def update_listboxes(self):
        self.despesas_listbox.delete(0, tk.END)
        for descricao, valor in self.despesas:
            self.despesas_listbox.insert(tk.END, f"{descricao}: R$ {valor:.2f}")
        
        self.receitas_listbox.delete(0, tk.END)
        for descricao, valor in self.receitas:
            self.receitas_listbox.insert(tk.END, f"{descricao}: R$ {valor:.2f}")

        self.selected_despesa_index = None
        self.selected_receita_index = None

        self.editar_despesa_button.config(state=tk.DISABLED)
        self.excluir_despesa_button.config(state=tk.DISABLED)
        self.editar_receita_button.config(state=tk.DISABLED)
        self.excluir_receita_button.config(state=tk.DISABLED)

    def save_data(self):
        data = {
            'despesas': self.despesas,
            'receitas': self.receitas
        }
        with open('financeiro_data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        if os.path.exists('financeiro_data.json'):
            with open('financeiro_data.json', 'r') as file:
                data = json.load(file)
                self.despesas = data.get('despesas', [])
                self.receitas = data.get('receitas', [])

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceiroApp(root)
    root.mainloop()
