import streamlit as st
import pandas as pd
import zipfile
import io

st.set_page_config(
    page_title="Fusion et analyse de fichiers CSV",
    page_icon="🔗",
    layout="wide"
)

def upload_files():
    """Composant pour uploader des fichiers ZIP"""
    uploaded_files = st.file_uploader(
        "Glissez-déposez vos fichiers ZIP ici",
        type=['zip'],
        accept_multiple_files=True,
        help="Uploadez un ou plusieurs fichiers ZIP contenant des fichiers CSV"
    )
    return uploaded_files

def merge_csv_files(uploaded_files):
    """Fusionne les fichiers CSV extraits des fichiers ZIP"""
    all_dataframes = []
    
    for uploaded_file in uploaded_files:
        try:
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                
                for csv_file in csv_files:
                    with zip_ref.open(csv_file) as file:
                        content = file.read()
                        # Lire avec l'encodage ISO-8859-1 et séparateur ;
                        df = pd.read_csv(
                            io.BytesIO(content),
                            encoding='ISO-8859-1',
                            sep=';',
                            quotechar='"',
                            dtype=str  # Garder tous les types comme string
                        )
                        all_dataframes.append(df)
                        st.info(f"✅ Fichier traité : {csv_file} ({len(df)} lignes)")
                        
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement de {uploaded_file.name}: {str(e)}")
    
    if all_dataframes:
        merged_df = pd.concat(all_dataframes, ignore_index=True, sort=False)
        return merged_df
    else:
        return None

def analyser_consommation_data(df):
    """Analyse la consommation de données et prépare la feuille 'Moyenne conso DATA'"""
    # Filtrer les lignes dont "Nom de la sous-rubrique" commence par "Echanges"
    if "Nom de la sous-rubrique" not in df.columns:
        st.error("❌ Colonne 'Nom de la sous-rubrique' manquante dans les données")
        return None
    
    # Corriger les valeurs NaN avant d'appliquer startswith
    df = df.copy()  # Créer une copie explicite du DataFrame
    df["Nom de la sous-rubrique"] = df["Nom de la sous-rubrique"].fillna("")
    filtered_df = df[df["Nom de la sous-rubrique"].str.startswith("Echanges")].copy()  # Créer une copie explicite
    
    if filtered_df.empty:
        st.warning("⚠️ Aucune donnée commençant par 'Echanges' trouvée")
        return None
    
    # Extraire les périodes de facturation et convertir en format date
    if "Période de la facture" not in filtered_df.columns:
        st.error("❌ Colonne 'Période de la facture' manquante dans les données")
        return None
    
    # Convertir la colonne de période au format date en utilisant .loc
    filtered_df.loc[:, "Date de facturation"] = pd.to_datetime(
        filtered_df["Période de la facture"],
        format="%d/%m/%Y", 
        errors="coerce"
    )
    
    # Créer une colonne pour le tri (format AAAAMM)
    filtered_df.loc[:, "Date_tri"] = filtered_df["Date de facturation"].dt.strftime("%Y%m")
    
    # Extraire le mois et l'année au format "mois-aa"
    filtered_df.loc[:, "Mois-Année"] = filtered_df["Date de facturation"].dt.strftime("%B-%y")
    
    # Traduire les noms des mois en français
    mois_fr = {
        'January': 'janvier', 'February': 'février', 'March': 'mars', 
        'April': 'avril', 'May': 'mai', 'June': 'juin',
        'July': 'juillet', 'August': 'août', 'September': 'septembre', 
        'October': 'octobre', 'November': 'novembre', 'December': 'décembre'
    }
    
    # Appliquer la traduction
    for en, fr in mois_fr.items():
        filtered_df.loc[:, "Mois-Année"] = filtered_df["Mois-Année"].str.replace(en, fr)
    
    # Colonnes fixes requises
    required_cols = [
        "Nom de la rubrique de niveau 1",
        "Numéro de l'utilisateur",
        "Nom de l'utilisateur",
        "Prénom de l'utilisateur",
        "Numéro de téléphone"
    ]
    
    # Vérifier que toutes les colonnes requises existent
    missing_cols = [col for col in required_cols if col not in filtered_df.columns]
    if missing_cols:
        st.error(f"❌ Colonnes manquantes: {', '.join(missing_cols)}")
        return None
    
    # Colonne pour les volumes
    volume_col = None
    possible_volume_cols = ["Volume consommé", "Volume Data", "Volume", "Quantité ou volume"]
    for col in possible_volume_cols:
        if col in filtered_df.columns:
            volume_col = col
            break
    
    if not volume_col:
        st.error("❌ Aucune colonne de volume trouvée")
        return None
    
    # Fonctions pour le traitement des volumes
    def parse_volume(vol_str):
        """Convertit une chaîne de volume en Go"""
        try:
            if isinstance(vol_str, (int, float)):
                return vol_str
            
            if pd.isna(vol_str) or vol_str == "":
                return 0
            
            total_bytes = 0
            
            # Gérer différents formats possibles
            if "Go" in vol_str and "Mo" in vol_str and "Ko" in vol_str:
                parts = vol_str.split()
                go_idx = parts.index("Go")
                mo_idx = parts.index("Mo")
                ko_idx = parts.index("Ko")
                
                go = float(parts[go_idx-1]) if go_idx > 0 else 0
                mo = float(parts[mo_idx-1]) if mo_idx > 0 else 0
                ko = float(parts[ko_idx-1]) if ko_idx > 0 else 0
                
                total_bytes = go * 1024 * 1024 * 1024 + mo * 1024 * 1024 + ko * 1024
            
            elif "Go" in vol_str and "Mo" in vol_str:
                parts = vol_str.split()
                go_idx = parts.index("Go")
                mo_idx = parts.index("Mo")
                
                go = float(parts[go_idx-1]) if go_idx > 0 else 0
                mo = float(parts[mo_idx-1]) if mo_idx > 0 else 0
                
                total_bytes = go * 1024 * 1024 * 1024 + mo * 1024 * 1024
            
            elif "Go" in vol_str:
                parts = vol_str.split()
                go_idx = parts.index("Go")
                go = float(parts[go_idx-1]) if go_idx > 0 else 0
                total_bytes = go * 1024 * 1024 * 1024
            
            elif "Mo" in vol_str:
                parts = vol_str.split()
                mo_idx = parts.index("Mo")
                mo = float(parts[mo_idx-1]) if mo_idx > 0 else 0
                total_bytes = mo * 1024 * 1024
                
            elif "Ko" in vol_str:
                parts = vol_str.split()
                ko_idx = parts.index("Ko")
                ko = float(parts[ko_idx-1]) if ko_idx > 0 else 0
                total_bytes = ko * 1024
            
            else:
                try:
                    total_bytes = float(vol_str)
                except:
                    return 0
                    
            return total_bytes / (1024 * 1024 * 1024)  # Conversion en Go
        except:
            return 0
    
    def format_volume(vol_go):
        """Convertit un volume en Go en format texte 'X Go Y Mo Z Ko'"""
        try:
            if pd.isna(vol_go) or vol_go == 0:
                return "0 Ko"
                
            go = int(vol_go)
            mo_decimal = (vol_go - go) * 1024
            mo = int(mo_decimal)
            ko = int((mo_decimal - mo) * 1024)
            
            result = ""
            if go > 0:
                result += f"{go} Go "
            if mo > 0:
                result += f"{mo} Mo "
            if ko > 0:
                result += f"{ko} Ko"
            
            return result.strip() if result else "0 Ko"
        except:
            return "0 Ko"
    
    # Appliquer la conversion en utilisant .loc
    filtered_df.loc[:, "Volume_Go"] = filtered_df[volume_col].apply(parse_volume)
    
    # Création d'une table de correspondance entre les mois-années et leurs dates de tri
    month_order = filtered_df.drop_duplicates("Mois-Année")[["Mois-Année", "Date_tri"]]
    month_order = dict(zip(month_order["Mois-Année"], month_order["Date_tri"]))
    
    # Ajouter les colonnes dynamiques par mois (pivot)
    pivot_df = filtered_df.pivot_table(
        index=required_cols,
        columns="Mois-Année",
        values="Volume_Go",
        aggfunc="sum",
        fill_value=0
    ).reset_index()
    
    # Trier les colonnes de mois du plus récent au plus ancien
    month_cols = [col for col in pivot_df.columns if col not in required_cols]
    month_cols = sorted(month_cols, key=lambda x: month_order.get(x, ""), reverse=True)
    pivot_df = pivot_df[required_cols + month_cols]
    
    # Créer la base du dataframe résultat
    result = pivot_df.copy()
    
    # Calculer le total en Go et les moyennes
    result["Volume_Total"] = result[month_cols].sum(axis=1)
    
    # Calculer les moyennes
    result["Volume_Moy_Total"] = result[month_cols].mean(axis=1)
    
    if len(month_cols) >= 4:
        result["Volume_Moy_4_Mois"] = result[month_cols[:4]].mean(axis=1)
    else:
        result["Volume_Moy_4_Mois"] = result["Volume_Moy_Total"]
    
    # Formater les totaux et moyennes en utilisant le même format que les volumes mensuels
    result["Total (Go)"] = result["Volume_Total"].apply(format_volume)
    result["Moyenne (Go) 4 mois"] = result["Volume_Moy_4_Mois"].apply(format_volume)
    result["Moyenne (Go) total"] = result["Volume_Moy_Total"].apply(format_volume)
    
    # Formater chaque colonne mensuelle
    for month in month_cols:
        result[month] = result[month].apply(format_volume)
    
    # Réorganiser les colonnes dans l'ordre final demandé
    final_cols = required_cols + ["Total (Go)", "Moyenne (Go) 4 mois", "Moyenne (Go) total"] + month_cols
    result = result[final_cols]
    
    # Supprimer les colonnes temporaires
    result = result.drop(columns=["Volume_Total", "Volume_Moy_Total", "Volume_Moy_4_Mois"], errors="ignore")
    
    return result

# Mise à jour de la fonction create_excel_file pour conserver uniquement les parties essentielles
def create_excel_file(dataframe, analysis_df=None):
    """
    Crée un fichier Excel contenant toutes les feuilles d'analyse
    """
    excel_buffer = io.BytesIO()
    
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        # 1. Feuille d'export standard (toujours en premier)
        dataframe.to_excel(
            writer,
            sheet_name='Export',
            index=False
        )
        
        # 2. Feuille d'analyse de consommation DATA (si disponible)
        if analysis_df is not None and not analysis_df.empty:
            analysis_df.to_excel(
                writer,
                sheet_name='Moyenne conso DATA',
                index=False
            )
            
            # Figer les volets en cellule F2
            worksheet = writer.sheets['Moyenne conso DATA']
            worksheet.freeze_panes = 'F2'
    
    excel_buffer.seek(0)
    return excel_buffer

def main():
    st.title("🔗 Fusion et analyse de fichiers CSV")
    st.markdown("---")
    
    # Zone de dépôt des fichiers
    uploaded_files = upload_files()
    
    if uploaded_files:
        st.success(f"{len(uploaded_files)} fichier(s) uploadé(s)")
        
        # Bouton pour démarrer la fusion
        if st.button("🚀 Démarrer la fusion et l'analyse", type="primary"):
            with st.spinner("Traitement en cours..."):
                try:
                    # Fusion des fichiers
                    merged_df = merge_csv_files(uploaded_files)
                    
                    if merged_df is not None and not merged_df.empty:
                        st.success(f"✅ Fusion terminée ! {len(merged_df)} lignes fusionnées")
                        
                        # Analyse des données pour la feuille "Moyenne conso DATA"
                        with st.spinner("Analyse des consommations DATA en cours..."):
                            analysis_df = analyser_consommation_data(merged_df)
                            
                            if analysis_df is not None and not analysis_df.empty:
                                st.success(f"✅ Analyse terminée ! {len(analysis_df)} utilisateurs analysés")
                            else:
                                st.warning("⚠️ Impossible de créer l'analyse des consommations DATA. Vérifiez le format des données.")
                        
                        # Création du fichier Excel avec toutes les feuilles
                        excel_buffer = create_excel_file(merged_df, analysis_df)
                        
                        # Un seul bouton de téléchargement
                        st.download_button(
                            label="📥 Télécharger Analyse de Parc.xlsx",
                            data=excel_buffer,
                            file_name="Analyse de Parc.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    else:
                        st.error("❌ Aucune donnée à fusionner")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors du traitement : {str(e)}")
                    st.exception(e)

if __name__ == "__main__":
    main()