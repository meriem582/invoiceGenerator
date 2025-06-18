# 🧾 InvoiceGenerator - Application Django

**InvoiceGenerator** est une application web développée avec **Django** qui permet de gérer des produits, créer des factures dynamiques et les exporter au format **PDF**. Simple, efficace et prête à l’emploi.

---

## 🌟 Fonctionnalités clés

- 🛍️ Gestion complète des **produits** (CRUD)
- 🧾 Création de **factures** à partir d’une sélection de produits
- 📥 Téléchargement de **factures en PDF** générées dynamiquement avec **ReportLab**
- 📄 Pagination intelligente des produits et des factures (groupe de 15/30/50)
- 🎨 Interface légère basée sur **Bootstrap minimalisé** + **CSS personnalisé**

---



## 🧱 Structure des données

| Modèle         | Description |
|----------------|-------------|
| `Product`      | Nom, prix, date d’expiration |
| `Invoice`      | Facture avec date de création, et ensemble d’`InvoiceItem`s |
| `InvoiceItem`  | Relie un produit à une facture avec une quantité (relation many-to-many) |

---

## 🗺️ Routes principales (URLs)

| Route                                      | Description |
|-------------------------------------------|-------------|
| `/`                                       | Tableau de bord |
| `/product/`                               | Liste des produits |
| `/product/AddProduct/`                    | Ajouter un produit |
| `/product/edit/<id>/`                     | Formulaire d’édition |
| `/product/edit/<id>/EditProduct/`         | Modifier un produit |
| `/product/deleteProduct/<id>/`            | Supprimer un produit |
| `/product/searchProduct/`                 | Rechercher un produit |
| `/invoice/`                               | Liste des factures |
| `/generateInvoice/`                       | Créer une facture (POST JSON) |
| `/invoice/deleteInvoice/<id>/`            | Supprimer une facture |
| `/invoice_details/<id>/`                  | Voir les détails d’une facture (JSON) |
| `/invoice/download_pdf/<id>/`             | Télécharger une facture PDF |

---

## 🎨 Interface utilisateur

- **Dashboard** : Vue d’accueil simplifiée
- **Produits** : Table avec pagination, tri par ID
- **Factures** : Liste des factures, consultation des détails, génération PDF
- **Design** : Basé sur `bootstrap.min.css` + `style.css` (personnalisé)
- **Interactions JS** : Dans `static/script.js` pour requêtes dynamiques

---

## 🧰 Technologies utilisées

- **Backend** : Python (3.8 est recomandé), Django
- **Frontend** : HTML, Bootstrap, CSS, JavaScript
- **PDF** : [ReportLab](https://www.reportlab.com/)
- **Base de données** : MySQL version 8.3

---

## ⚙️ Installation & Lancement

```bash
# 1. Cloner le projet
git clone https://github.com/meriem582/invoiceGenerator.git
cd invoiceGenerator

# 3. Création d'une base de données 
create database InvoiceGeneratorDB

# 2. Remplir la base de données par les tables défini dans models.py
python manage.py makemigration

# 3. Appliquer les migrations
python manage.py migrate

# 4. Lancer le serveur
python manage.py runserver

Puis rendez-vous sur http://127.0.0.1:8000