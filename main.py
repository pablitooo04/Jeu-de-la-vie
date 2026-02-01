from tkinter import *

dico_couleurs = {
    0: "#FFFFFF",
    1: "#000000",
}

auto_mode = False

def boucle_auto():
    global auto_mode
    if auto_mode:
        I1.avance()
        root.after(150, boucle_auto)  # avance toutes les 300 ms
n_tableau = 27
tableau = [[0 for _ in range(n_tableau)] for _ in range(n_tableau)]

window_size = 820

root = Tk()
root.geometry(f"{window_size}x{window_size}")
root.resizable(False, False)
root.title("Jeu de la vie")

canvas = Canvas(width = window_size, height = window_size)

class Interface:
    def __init__(self, tableau, taille):
        self.tableau = tableau
        self.taille = taille
        self.edit_mode = False
        self.intervalle = self.taille/len(self.tableau)
        for i in range(len(self.tableau) + 1):
            pos = int(i * self.intervalle)
            canvas.create_line(pos, 0, pos, self.taille, fill="#C7C6C6")
            canvas.create_line(0, pos, self.taille, pos, fill="#C7C6C6")

        
        for n_ligne in range(len(self.tableau)):
            for n_case in range(len(self.tableau)):
                if self.tableau[n_ligne][n_case] != 0:
                    canvas.create_rectangle(
                        int(n_case * self.intervalle),
                        int(n_ligne * self.intervalle),
                        int((n_case + 1) * self.intervalle),
                        int((n_ligne + 1) * self.intervalle),
                        fill=dico_couleurs[self.tableau[n_ligne][n_case]],
                        outline="#C7C6C6"
                    )

        canvas.place(x=0, y=0)
        
    
    def liste_voisins(self, C):
        """
        retourne la liste des voisins de la case C

        """
        l = []
        dic = {0: 0, 1: 0}
        for addition_x in [-1, 0, 1]:
            for addition_y in [-1, 0, 1]:
                if C[0]+addition_x in range(0, len(self.tableau)) and C[1] + addition_y in range(0, len(self.tableau)) and (C[0]+addition_x, C[1]+addition_y) != C:
                    l.append((C[0]+addition_x, C[1]+addition_y))
        
        for voisin in l:
            dic[self.tableau[voisin[0]][voisin[1]]] += 1

        return [l, dic]
    
    def avance(self):
        self.tableau_temp = [[0 for _ in range(len(self.tableau))] for _ in range(len(self.tableau))]
        for lignes in range(len(self.tableau)):
            for cases in range(len(self.tableau)):
                if self.tableau[lignes][cases] == 0 and self.liste_voisins((lignes, cases))[1][1] == 3:
                    self.tableau_temp[lignes][cases] = 1
                elif self.tableau[lignes][cases] == 1 and self.liste_voisins((lignes, cases))[1][1] in [2, 3]:
                    self.tableau_temp[lignes][cases] = 1
                elif self.tableau[lignes][cases] == 1 and self.liste_voisins((lignes, cases))[1][1] not in [2, 3]:
                    self.tableau_temp[lignes][cases] = 0
        self.tableau = self.tableau_temp
        self.actualiser(self.tableau_temp)
        
    def actualiser(self, T):
        canvas.delete("all")
        for i in range(len(self.tableau) + 1):
            pos = int(i * self.intervalle)
            canvas.create_line(pos, 0, pos, self.taille, fill="#C7C6C6")
            canvas.create_line(0, pos, self.taille, pos, fill="#C7C6C6")
        
        self.nouveau_tab = T
        for n_ligne in range(len(self.nouveau_tab)):
            for n_case in range(len(self.nouveau_tab)):
                if self.nouveau_tab[n_ligne][n_case] != 0:
                    canvas.create_rectangle(
                        int(n_case * self.intervalle),
                        int(n_ligne * self.intervalle),
                        int((n_case + 1) * self.intervalle),
                        int((n_ligne + 1) * self.intervalle),
                        fill=dico_couleurs[self.nouveau_tab[n_ligne][n_case]],
                        outline="#C7C6C6"
)

                    
    def edit(self):
        if not auto_mode:
            if not I1.edit_mode:
                self.edit_mode = True
                canvas.configure(bg="#7799d1")
            else:
                self.edit_mode = False
                canvas.configure(bg="#f6f6f6")

def clique(event):
    if not auto_mode:
        if not I1.edit_mode:
            I1.avance()
        else:
            case = (
                min(int(event.x / I1.intervalle), len(I1.tableau[0]) - 1),
                min(int(event.y / I1.intervalle), len(I1.tableau) - 1),
                    )
            I1.tableau[case[1]][case[0]] = 1
            canvas.create_rectangle(int(case[0]*I1.intervalle), int(case[1]*I1.intervalle), int((case[0]+1)*I1.intervalle), int((case[1]+1)*I1.intervalle), fill=dico_couleurs[1])

def toggle_auto(event=None):
    global auto_mode
    if not I1.edit_mode:
        auto_mode = not auto_mode
        if auto_mode:
            boucle_auto()

if __name__ == "__main__":
    I1 = Interface(tableau, window_size)
    root.bind("<space>", toggle_auto)
    canvas.bind("<Button-1>", clique)
    canvas.bind("<Button-3>", lambda event: I1.edit())

    root.mainloop()
    

