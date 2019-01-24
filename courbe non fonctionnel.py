
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import random
import serial
import time

NB_POINTS_MAX = 100  # Un maximum de NB_POINTS_MAX seront dessinés
MAX_Y = 1023         # Dont l'ordonnée sera comprise entre 0 et MAX_Y (valeur aléatoire)



class Fenetre(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Fenetre, self).__init__()
        loadUi('IHM.ui', self)
        self.lesX = []
        self.lesY = []
        self.nbPts = 0
        self.genereCourbe()
        self.btnAcquisition.clicked.connect(self.ajoutPoints)

    def genereCourbe(self):
        # generate the plot
        self.ax = self.graphicsView.canvas.ax
        # set specific limits for X and Y axes
        self.ax.set_xlim(1, NB_POINTS_MAX)
        self.ax.set_ylim(0, MAX_Y)
        self.ax.set_autoscale_on(False)
        self.courbe, = self.ax.plot(self.lesX, self.lesY,label="ma courbe")
        # generate the canvas to display the plot
        self.graphicsView.canvas.draw()

    def ajoutPoints(self):  # Appelée à chaque clic sur le bouton
        
        ser = serial.Serial('COM4' , 19200) 
        time.sleep(5)
        print("debut")
        while True:
            ch = ser.readline()
            self.nbPts += 1
            self.lesX.append(self.nbPts)  # Ajout d'une nouvelle abscisse
            self.lesY.append(ch) # Ajout d'une nouvelle ordonnée
            if len(self.lesX) > NB_POINTS_MAX: # Si on dépasse le nb de points à afficher...
                self.lesX = self.lesX[1:] # Suppression du premier élément pour avoir une fenêtre glissante
                self.lesY = self.lesY[1:]
                self.ax.set_xlim(self.nbPts - NB_POINTS_MAX + 1, self.nbPts) # On réajuste l'échelle de l'axe des X
            self.courbe.set_data(self.lesX, self.lesY) # On met à jour les nouveaux couples de points à afficher
            self.graphicsView.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Fenetre()
    win.show()
    app.exec_()
