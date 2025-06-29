# 🐘 ARIMA - Implementación del juego Arimaa con IA (Minimax)

**ARIMA** es una implementación del juego de estrategia **Arimaa**, desarrollada en Python. Este proyecto replica la mayoria de las reglas oficiales del juego, incluyendo empujar, trampas y congelamiento de piezas. Además, incluye una **inteligencia artificial basada en el algoritmo Minimax**, con heurísticas personalizadas para evaluar estados del juego y tomar decisiones competitivas.

---

## 🎯 Objetivo del Proyecto

- Reproducir el juego de mesa **Arimaa**, creado como alternativa al ajedrez pero más difícil de dominar por una IA.
- Implementar desde cero:
  - La **lógica de juego**
  - Las **reglas oficiales**
  - La **IA con Minimax**
  - Una **interfaz gráfica interactiva**
- Explorar el desarrollo de algoritmos de IA aplicados a juegos de estrategia de alto nivel.

---

## 📚 Sobre Arimaa

Arimaa es un juego de estrategia para dos jugadores sobre un tablero 8×8 con reglas similares al ajedrez, pero con una estructura que dificulta la resolución por fuerza bruta. Las reglas clave incluyen:

- Cada jugador dispone de 16 piezas: elefante, camello, caballos, perros, gatos y conejos.
- Las piezas más fuertes pueden **empujar** o **tirar** a las más débiles.
- El tablero incluye **casillas trampa** (c3, f3, c6, f6) que eliminan piezas sin apoyo.
- Las piezas pueden **quedar congeladas** si están junto a una más fuerte sin apoyo aliada.
- El objetivo es llevar un conejo a la fila de inicio del oponente o inmovilizarlo.

Más información sobre las reglas: [Reglas de Arimaa (Wikilibros)](https://es.wikibooks.org/wiki/Arimaa/Información/Reglas)

---

## 📁 Estructura del Proyecto

```
PROYECTO-ARIMA/
├── assets/             # Imágenes o recursos multimedia
├── src/
│   ├── main.py         # Punto de entrada principal
│   ├── game.py         # Mecánicas de turno, verificación de condiciones
│   ├── logica.py       # Reglas: movimientos, trampas, empujar, tirar
├── requerimientos.txt  # Dependencias del proyecto
└── .git/               # Control de versiones
```

---

## ⚙️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/JuanCa-16/PROYECTO-ARIMA.git
cd PROYECTO-ARIMA
```

2. Crea un entorno virtual y actívalo:
```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
.\venv\Scripts\activate      # Windows
```

3. Instala las dependencias:
```bash
pip install -r requerimientos.txt
```

---

## 🚀 Ejecución

Para iniciar el juego, ejecuta:

```bash
python src/main.py
```

---

## 🧠 Inteligencia Artificial

El motor de IA utiliza el algoritmo **Minimax**, implementado con las siguientes características:

- Exploración de estados posibles hasta una profundidad configurable.
- Heurística que evalúa:
  - Diferencia de conejos vivos.
  - Piezas en casillas trampa.
  - Conejo más cercano a la meta.
  - Piezas congeladas.
- Posible mejora futura con poda alfa-beta y refinamiento de heurísticas.

---

## 🧰 Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **IA:** Algoritmo Minimax (sin uso de bibliotecas externas de IA)
- **Interfaz Gráfica:** `pygame`

---

## 📌 Estado del Proyecto

✔️ Juego completamente funcional  
✔️ Mayoria de las reglas oficiales implementadas  
✔️ IA funcional con Minimax  
🔧 Pendiente: optimización de heurísticas y rendimiento

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como ejercicio académico.

---

## 👥 Autores

- Juan Camilo Henao
- Juan Manuel Valencia
- Isabella Rebellon Medina
