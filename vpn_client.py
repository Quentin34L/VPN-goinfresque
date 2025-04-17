# Création de l'interface graphique pour le VPN

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
import requests

class VPNApp(QWidget):
    def __init__(self):
        super().__init__()

        # Création de l'interface
        self.setWindowTitle("VPN Goinfresque")
        self.setGeometry(500, 500, 300, 300)

        self.layout = QVBoxLayout()

        # Afficher bouton "Connect"
        self.button = QPushButton("Connect")
        self.button.clicked.connect(self.toggle_vpn)
        self.layout.addWidget(self.button)

        # Bouton "Status"
        self.status_button = QPushButton("Off") 
        self.layout.addWidget(self.status_button)

        # Styliser le bouton "Status"
        self.apply_button_style(self.status_button)

        # Label pour afficher l'état
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # Bouton "Show IP"
        self.show_ip_button = QPushButton("Show IP")
        self.show_ip_button.clicked.connect(self.show_ip)
        self.show_ip_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 16px;    
            }
            QPushButton:hover {
                background-color: #444;  /* Gris plus foncé au survol */
            }
        """)
        self.layout.addWidget(self.show_ip_button)

        # Label pour afficher l'IP
        self.ip_label = QLabel("")  # L'IP sera affichée ici
        self.layout.addWidget(self.ip_label)

        self.setLayout(self.layout)

        # Appliquer l'ombre et l'animation au bouton
        self.apply_button_shadow()
        self.setup_button_animation()

        # Appliquer style initial du bouton (Connect)
        self.apply_button_style(self.button)

    # Styliser le bouton (noir avec texte blanc)
    def apply_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: black;  /* Noir pour le bouton */
                color: white;  /* Texte blanc */
                border-radius: 12px;  /* Bords arrondis */
                padding: 10px 20px;  /* Espace autour du texte */
                font-size: 16px;  /* Taille du texte */
            }
            QPushButton:hover {
                background-color: #444;  /* Gris plus foncé au survol */
            }
        """)

    # Appliquer une ombre douce au bouton
    def apply_button_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)  # Rayon du flou
        shadow.setOffset(5, 5)    # Décalage de l'ombre
        shadow.setColor(Qt.GlobalColor.black)  # Ombre noire
        self.button.setGraphicsEffect(shadow)
        self.status_button.setGraphicsEffect(shadow)

    # Configurer l'animation du bouton (zoom lors du survol)
    def setup_button_animation(self):
        self.anim = QPropertyAnimation(self.button, b"pos")
        self.anim.setDuration(200)  # Durée de l'animation en ms
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)  # Courbe de l'animation

    # Fonction de changement d'affichage (Connect/Disconnect)
    def toggle_vpn(self):
        if self.button.text() == "Connect":
            self.status_button.setText("Status : On")  # Changer à "On" lorsque connecté
            self.button.setText("Disconnect")

            # Changer le fond de la fenêtre en vert
            self.setStyleSheet("background-color: #33e333;")  # Fond vert

        else:
            self.status_button.setText("Status : Off")  # Changer à "Off" lorsque déconnecté
            self.button.setText("Connect")

            # Changer le fond de la fenêtre en rouge
            self.setStyleSheet("background-color: #f03f3f;")  # Fond rouge

    # Fonction pour afficher l'IP publique
    def show_ip(self):
        # Vérifier si l'IP est déjà affichée, si oui, la cacher
        if self.ip_label.text():
            self.ip_label.setText("")  # Masquer l'IP
        else:
            ip = self.get_public_ip()
            self.ip_label.setText(f"Your IP : {ip}")  # Afficher l'IP sous le bouton "Show IP"

    # Récupérer l'IP publique de l'utilisateur
    def get_public_ip(self):
        try:
            return requests.get("http://api64.ipify.org").text
        except:
            return "Unable to fetch IP"


# Lancement du programme
if __name__ == "__main__":
    app = QApplication([])
    window = VPNApp()
    window.show()
    app.exec()
