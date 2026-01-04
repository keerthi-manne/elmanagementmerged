from your_app import create_app, mysql

app = create_app()

def debug_themes():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🔍 Debugging Themes & Projects...")
        
        # 1. Get Themes
        cur.execute("SELECT ThemeID, ThemeName FROM Theme")
        themes = cur.fetchall()
        theme_map = {t[1]: t[0] for t in themes}
        valid_theme_ids = set(theme_map.values())
        
        print(f"   Found {len(themes)} themes:")
        for t in themes:
            print(f"    - ID {t[0]}: {t[1]}")
            
        # 2. Get Projects
        cur.execute("SELECT ProjectID, Title, ThemeID FROM Project")
        projects = cur.fetchall()
        
        print(f"\n   Found {len(projects)} projects:")
        projects_to_fix = []
        
        for p in projects:
            pid, title, tid = p
            status = "✅ Valid" if tid in valid_theme_ids else "❌ INVALID THEME"
            if tid not in valid_theme_ids:
                projects_to_fix.append(pid)
            print(f"    - ID {pid}: {title[:30]}... (ThemeID: {tid}) -> {status}")
            
        # 3. Fix Logic
        if projects_to_fix:
            print(f"\n🔧 Fixing {len(projects_to_fix)} projects with invalid themes...")
            
            # Use 'Machine Learning' as default if available, else first theme
            default_theme_id = theme_map.get('Machine Learning') or themes[0][0]
            print(f"   Targeting Theme ID: {default_theme_id} (Machine Learning or fallback)")
            
            for pid in projects_to_fix:
                try:
                    cur.execute("UPDATE Project SET ThemeID = %s WHERE ProjectID = %s", (default_theme_id, pid))
                except Exception as e:
                    print(f"   Failed to fix project {pid}: {e}")
            
            mysql.connection.commit()
            print("✅ Fixed invalid projects.")
        else:
            print("\n✅ All projects have valid themes. (If dashboard is empty, check Faculty assignment)")

        # 4. Check 'Machine Learning' specifically (since Merin is assigned there)
        ml_id = theme_map.get('Machine Learning')
        if ml_id:
            cur.execute("SELECT COUNT(*) FROM Project WHERE ThemeID = %s", (ml_id,))
            count = cur.fetchone()[0]
            print(f"\n📊 Projects in 'Machine Learning' (ID {ml_id}): {count}")
            
            if count == 0:
                print("⚠️ No projects in Machine Learning! Moving some projects there for the demo...")
                # Move first 3 projects to ML
                ids_to_move = [p[0] for p in projects[:3]]
                for pid in ids_to_move:
                     cur.execute("UPDATE Project SET ThemeID = %s WHERE ProjectID = %s", (ml_id, pid))
                mysql.connection.commit()
                print(f"   ✅ Moved {len(ids_to_move)} projects to Machine Learning.")
        
        cur.close()

if __name__ == "__main__":
    debug_themes()
