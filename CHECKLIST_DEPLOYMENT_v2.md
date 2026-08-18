# ✅ CHECKLIST ACTUALIZADO: Desplegar FixCellGt en Vercel (v2.0)

## 🔧 Qué Fue Arreglado

✓ Removimos el error de `uv pip install`
✓ Creamos estructura correcta: `/api/index.py`
✓ Actualizamos `vercel.json` con configuración correcta
✓ Optimizamos `requirements.txt`

---

## 📁 Estructura de Archivos Correcta

```
fixcellgt-web/
├── buscador_web.html          ← Página principal
├── requirements.txt            ← Dependencias Python
├── vercel.json                ← Config Vercel (ACTUALIZADO)
├── .vercelignore              ← Archivos a ignorar
└── api/
    └── index.py               ← API REST (NUEVO)
```

---

## 🚀 PASO 1: Push a GitHub

```bash
# Navega a tu carpeta
cd C:\Users\FixCellGt\Documents\Proyectos\varios\fixcellgt-inventario\web

# Agregar archivos nuevos
git add .

# Commit
git commit -m "Corregir deployment Vercel - estructura serverless correcta"

# Push
git push origin main
```

---

## 🌐 PASO 2: Vercel Settings (Variables de Entorno)

### 2.1 - Ir a Settings

1. Ve a tu proyecto en https://vercel.com/dashboard
2. Click en **Settings → Environment Variables**

### 2.2 - Eliminar Variables Anteriores

1. Si hay variables en **rojo** o con error, click en el `-` para eliminarlas
2. Limpia todo lo anterior

### 2.3 - Agregar 5 Variables NUEVAS

**Cada variable:**
- Type: **Plain** (NO Secret) ✓
- Click **Save**

```
Variable 1:
Key:   SUPABASE_DB_HOST
Value: db.vouzslwrthiqtnahdsu.supabase.co
Type:  Plain ✓

Variable 2:
Key:   SUPABASE_DB_PORT
Value: 5432
Type:  Plain ✓

Variable 3:
Key:   SUPABASE_DB_NAME
Value: postgres
Type:  Plain ✓

Variable 4:
Key:   SUPABASE_DB_USER
Value: postgres
Type:  Plain ✓

Variable 5:
Key:   SUPABASE_DB_PASSWORD
Value: (tu contraseña de Supabase)
Type:  Plain ✓
```

⚠️ **CRÍTICO:** Asegúrate que cada una diga **"Plain"**, no "Secret"

---

## 🔄 PASO 3: Hacer Deploy

### Opción A: Deploy Automático (Recomendado)
1. Vercel automáticamente detecta el push a GitHub
2. Inicia el build automáticamente
3. Espera 3-5 minutos

### Opción B: Deploy Manual
1. En tu proyecto Vercel
2. Click en **"Redeploy"** (arriba a la derecha)
3. Selecciona **"main"**
4. Click **"Redeploy"**

---

## ✅ PASO 4: Verificar Deploy

### 4.1 - Esperar a que Termine
- Debes ver **"Deployment Successful"** (verde)
- Si ves rojo, mira los **Deploy Logs** y busca el error

### 4.2 - Obtener URLs

En el dashboard de Vercel:
```
Tu dominio es algo como:
https://fixcellgt-web-xyz123.vercel.app
```

---

## 🔗 PASO 5: Actualizar Frontend

1. Abre **`buscador_web.html`** en tu editor
2. Busca esta línea (línea ~368):
   ```javascript
   const API_URL = 'http://localhost:5000/api';
   ```
3. Reemplázala con tu URL de Vercel:
   ```javascript
   const API_URL = 'https://fixcellgt-web-xyz123.vercel.app/api';
   ```
4. Guarda el archivo
5. Haz push a GitHub:
   ```bash
   git add buscador_web.html
   git commit -m "Actualizar URL de API"
   git push origin main
   ```

Vercel re-deployará automáticamente en 1-2 minutos.

---

## 🧪 PASO 6: Probar la API

### Test 1: Verificar Health Check
```
URL: https://fixcellgt-web-xyz123.vercel.app/api

Abre en navegador:
→ Deberías ver: {"status": "ok", "message": "FixCellGt API v1.0"}
```

### Test 2: Obtener Marcas
```
URL: https://fixcellgt-web-xyz123.vercel.app/api/marcas

Esperado: ["Apple", "Samsung", "Huawei", ...]
```

### Test 3: Buscar Inventario
```
URL: https://fixcellgt-web-xyz123.vercel.app/api/inventario/buscar?marca=Apple&repuesto=Pantalla

Esperado: Array con resultados
```

---

## 🌍 PASO 7: ¡Acceso Público!

Tu buscador ahora está en internet:

```
🔧 FixCellGt Buscador: https://fixcellgt-web-xyz123.vercel.app

Puedes compartir esta URL con cualquiera
```

---

## ✅ Verificación Final

Marca los que completaste:

- [ ] Push a GitHub con archivos actualizados
- [ ] Variables de entorno agregadas en Vercel (tipo "Plain")
- [ ] Deploy completado sin errores (verde)
- [ ] API `/api` devuelve OK
- [ ] API `/api/marcas` devuelve lista
- [ ] URL de API actualizada en `buscador_web.html`
- [ ] HTML se carga correctamente en navegador
- [ ] Búsquedas devuelven resultados

---

## 🆘 Troubleshooting

### ❌ "Build Failed: Command 'uv pip install' exited with 1"
**Solución:** 
- Los archivos han sido actualizados
- Haz un nuevo push a GitHub
- Vercel debería construir correctamente ahora

### ❌ "Cannot find module"
**Solución:**
```bash
# Verifica requirements.txt esté en la carpeta raíz
# Reconstruye en Vercel: Settings → Redeploy
```

### ❌ "Cannot connect to database"
**Solución:**
- Abre Vercel Settings → Environment Variables
- Verifica que las 5 variables estén agregadas
- Verifica credenciales de Supabase son correctas
- Las variables deben ser tipo "Plain"

### ❌ "CORS error / API no responde"
**Solución:**
- Verifica la URL de API en `buscador_web.html`
- Abre navegador → F12 → Console
- Busca errores de fetch
- Prueba directamente: `https://fixcellgt-web-xyz123.vercel.app/api`

### ❌ "Página en blanco"
**Solución:**
- Abre F12 → Console
- Busca errores JavaScript
- Verifica que API_URL sea correcta
- Limpia cache: Ctrl+Shift+Del

---

## 📞 Próximos Pasos (Después de Deployment)

1. **Dominio Personalizado** (Opcional)
   - Vercel Settings → Domains
   - Conecta tu dominio propio

2. **Analytics**
   - Vercel Dashboard → Analytics
   - Ver quién usa tu buscador

3. **Automatización** (Ya tienes scripts)
   - `automatizar_actualizaciones.py`
   - Sincroniza datos automáticamente

---

**¿Listo? Comienza por el PASO 1** ⬆️
