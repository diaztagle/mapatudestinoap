# mapapp.py

import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import base64
import os
from typing import Dict, List

# --- Configuración inicial ---
st.set_page_config(page_title="Domina Tu Destino", page_icon="🌟", layout="wide")

# --- Traducciones ---
translations = {
    "en": {
        "header.title": "Domina Tu Destino",
        "header.subtitle": "Unveiling insights through chirology and numerology.",
        "form.title": "Your Consultation",
        "form.question.label": "1. What question or concern is on your mind? (e.g., career, relationships)",
        "form.question.placeholder": "Tell me about my creative path...",
        "form.birthdate.label": "2. What is your date of birth?",
        "form.birthdate.error.future": "Birth date cannot be in the future.",
        "uploader.title": "Your Hands' Story",
        "uploader.instruction": "3. Upload 1-4 clear photos of your hands (e.g., left/right palm, back of hand).",
        "uploader.upload.button": "Upload files",
        "uploader.upload.drag": "or drag and drop",
        "uploader.upload.info": "PNG, JPG, GIF up to 10MB each",
        "uploader.uploaded.title": "Uploaded Images:",
        "uploader.uploaded.success": "Successfully uploaded",
        "uploader.guide.button": "View Photo Guide",
        "uploader.guide.title": "Guide to Taking Good Hand Photos",
        "uploader.guide.intro": "For the most accurate reading, high-quality images are essential. Follow these tips to take clear, detailed photos of your hands:",
        "uploader.guide.modal.close": "Got it",
        "uploader.guide.examples.title": "Visual Examples",
        "uploader.guide.examples.good": "Good",
        "uploader.guide.examples.bad": "Bad",
        "uploader.guide.examples.lighting.title": "1. Lighting",
        "uploader.guide.examples.lighting.good": "Use bright, natural daylight near a window. Lines are clear and easy to see.",
        "uploader.guide.examples.lighting.bad": "Avoid direct sunlight, flash, or dim rooms which create hard shadows or wash out details.",
        "uploader.guide.examples.focus.title": "2. Focus",
        "uploader.guide.examples.focus.good": "Tap your screen to focus on the palm. Every major and minor line should be sharp.",
        "uploader.guide.examples.focus.bad": "The image is out of focus, making the lines impossible to analyze accurately.",
        "uploader.guide.examples.angle.title": "3. Angle",
        "uploader.guide.examples.angle.good": "Hand is relaxed and flat, filling the frame. All fingers and the base of the palm are visible.",
        "uploader.guide.examples.angle.bad": "Fingers are curled, hand is at a steep angle, or parts of the hand are cut off.",
        "uploader.guide.mistakes.title": "Common Mistakes & How to Fix Them",
        "uploader.guide.mistakes.point1": "Too blurry: Before taking the photo, tap the center of your palm on your phone screen to set the focus.",
        "uploader.guide.mistakes.point2": "Harsh shadows: Don't use your phone's flash. Move near a window for soft, natural light instead.",
        "uploader.guide.mistakes.point3": "Cluttered background: Place your hand on a plain, dark surface like a table or a piece of paper.",
        "uploader.guide.mistakes.point4": "Wrong angle: Hold your phone directly above your hand, parallel to your palm, to avoid distortion.",
        "uploader.guide.angles.title": "The 4 Essential Photos",
        "uploader.guide.angles.point1": "Dominant Hand Palm: A clear, centered shot of your entire palm, from wrist to fingertips.",
        "uploader.guide.angles.point2": "Non-Dominant Hand Palm: A clear shot of your other palm, for a complete picture.",
        "uploader.guide.angles.point3": "Side of Dominant Hand (Percussion): A view of the side of your hand below the little finger.",
        "uploader.guide.angles.point4": "Back of Dominant Hand: Shows finger shape, length, and nails.",
        "disclaimer.title": "A Note on Your Journey",
        "disclaimer.text": "This analysis is intended for self-reflection and entertainment. It is an orientational guide for self-knowledge, not a substitute for professional, medical, or legal advice. Your future is shaped by your choices.",
        "button.submit": "Reveal My Path",
        "button.new": "Start a New Consultation",
        "loader.title": "Consulting the Cosmos...",
        "loader.text": "Elara is interpreting the patterns of your destiny. Please wait a moment.",
        "result.title": "Your Path Illuminated",
        "error.missingFields": "Please fill out all fields and upload at least one hand image.",
        "error.apiError": "An error occurred while generating your reading. Please try again.",
        "error.apiKeyMissing": "API Key is not configured. Please set the API_KEY environment variable.",
        "warning.apiKeyMissing": "Warning: API Key is not configured. This application will not work without it.",
        "footer.text": "© {year} Domina Tu Destino. For self-discovery purposes.",
        "auth.title": "Begin Your Journey",
        "auth.login.tab": "Log In",
        "auth.signup.tab": "Sign Up",
        "auth.email.label": "Email Address",
        "auth.password.label": "Password",
        "auth.login.button": "Log In",
        "auth.signup.button": "Sign Up",
        "auth.or": "Or continue with",
        "auth.google.button": "Sign in with Google",
        "auth.toggle.login": "Already have an account? Log In",
        "auth.toggle.signup": "Don't have an account? Sign Up",
        "auth.error.invalidCredentials": "Invalid email or password.",
        "auth.error.emailInUse": "This email is already in use.",
        "auth.error.generic": "An error occurred. Please try again.",
        "auth.error.invalidEmail": "Please enter a valid email address.",
        "auth.error.passwordComplexity": "Password does not meet the requirements.",
        "auth.password.requirements": "Must be 8+ characters and include an uppercase letter, a number, and a special character.",
        "auth.forgotPassword.link": "Forgot Password?",
        "auth.reset.title": "Reset Password",
        "auth.reset.button": "Send Reset Link",
        "auth.reset.successMessage": "If an account with that email exists, a password reset link has been sent.",
        "auth.reset.backButton": "Back to Login",
        "profile.logout": "Log Out",
        "profile.menu.profile": "My Profile",
        "profile.menu.settings": "Settings",
        "profile.menu.contact": "Contact Angel",
        "profile.menu.contact.email": "By Email",
        "profile.menu.contact.immediate": "Immediately",
        "profile.menu.contact.whatsapp": "By WhatsApp",
        "profile.title": "My Profile",
        "profile.displayName.label": "Display Name",
        "profile.email.label": "Email Address",
        "profile.save.button": "Save Changes",
        "profile.back.button": "Back to Consultation",
        "profile.consultantId.label": "Consultant Member ID",
        "profile.success": "Profile updated successfully!",
        "profile.error": "Failed to update profile. Please try again.",
        "profile.error.fileRead": "Failed to read image file. Please try another image.",
        "profile.history.title": "Consultation History",
        "profile.history.empty.title": "Your Story Awaits",
        "profile.history.empty.description": "Your journey of self-discovery begins with a single question. Start your first consultation to illuminate your path.",
        "profile.history.empty.button": "Start My First Reading",
        "profile.history.questionLabel": "Question:",
        "profile.history.viewButton": "View Reading",
        "result.contact.title": "Need a Deeper Interpretation?",
        "result.contact.button": "Contact Angel",
        "result.contact.message": "Send a Message",
        "result.messageModal.title": "Send a Message to Angel",
        "result.messageModal.placeholder": "Type your message here...",
        "result.messageModal.send": "Send Message",
        "result.table.download": "Download Table",
        "result.table.download.csv": "Download as CSV",
        "result.table.download.xlsx": "Download as Excel (.xlsx)",
        "result.table.download.pdf": "Download as PDF",
        "result.table.download.png": "Download as Image (PNG)",
        "result.table.caption": "Detailed analysis data.",
        "result.lifeCycleChart.title": "The Cycles of Your Life Path",
        "result.lifeCycleChart.period": "Period",
        "result.lifeCycleChart.mainFocus": "Main Focus",
        "result.lifeCycleChart.keyAdvice": "Key Advice",
        "result.save.button": "Save to History",
        "result.save.saved": "Saved to History",
        "result.copy.button": "Copy to clipboard",
        "result.copy.copied": "Copied!",
        "result.export.button": "Export Analysis",
        "result.export.text": "Export as Text (.txt)",
        "result.export.markdown": "Export as Markdown (.md)",
        "result.export.pdf": "Export as PDF",
        "settings.title": "Settings",
        "settings.language.title": "Language Preferences",
        "settings.language.description": "Choose the language for the application interface.",
        "settings.notifications.title": "Notification Settings",
        "settings.notifications.consultationReady": "Consultation Ready",
        "settings.notifications.promotionalOffers": "Promotional Offers",
        "settings.account.title": "Account Management",
        "settings.account.delete.description": "Permanently delete your account and all associated data. This action cannot be undone.",
        "settings.account.delete.button": "Delete Account",
        "settings.modal.delete.title": "Confirm Account Deletion",
        "settings.modal.delete.text": "Are you sure you want to permanently delete your account? All your data will be lost.",
        "settings.modal.delete.confirm": "Delete",
        "settings.modal.delete.cancel": "Cancel",
        "modal.confirm.title": "Confirm Your Consultation",
        "modal.confirm.text": "Are you ready to submit your consultation? Please review the details below.",
        "modal.confirm.questionLabel": "Your Question:",
        "modal.confirm.birthDateLabel": "Your Birth Date:",
        "modal.confirm.imagesLabel": "Hand Images:",
        "modal.confirm.imageCount": "{count} images uploaded",
        "modal.confirm.confirmButton": "Submit",
        "modal.confirm.cancelButton": "Cancel"
    },
    "es": {
        "header.title": "Domina Tu Destino",
        "header.subtitle": "Revelando percepciones a través de la quirología y la numerología.",
        "form.title": "Tu Consulta",
        "form.question.label": "1. ¿Qué pregunta o inquietud tienes en mente? (ej., carrera, relaciones)",
        "form.question.placeholder": "Háblame de mi camino creativo...",
        "form.birthdate.label": "2. ¿Cuál es tu fecha de nacimiento?",
        "form.birthdate.error.future": "La fecha de nacimiento no puede estar en el futuro.",
        "uploader.title": "La Historia de Tus Manos",
        "uploader.instruction": "3. Sube de 1 a 4 fotos nítidas de tus manos (ej., palma izquierda/derecha, dorso).",
        "uploader.upload.button": "Subir archivos",
        "uploader.upload.drag": "o arrastra y suelta",
        "uploader.upload.info": "PNG, JPG, GIF de hasta 10MB cada uno",
        "uploader.uploaded.title": "Imágenes Subidas:",
        "uploader.uploaded.success": "Subida con éxito",
        "uploader.guide.button": "Ver Guía de Fotos",
        "uploader.guide.title": "Guía para Tomar Buenas Fotos de Manos",
        "uploader.guide.intro": "Para la lectura más precisa, es esencial tener imágenes de alta calidad. Sigue estos consejos para tomar fotos nítidas y detalladas de tus manos:",
        "uploader.guide.modal.close": "Entendido",
        "uploader.guide.examples.title": "Ejemplos Visuales",
        "uploader.guide.examples.good": "Bien",
        "uploader.guide.examples.bad": "Mal",
        "uploader.guide.examples.lighting.title": "1. Iluminación",
        "uploader.guide.examples.lighting.good": "Usa luz natural y brillante cerca de una ventana. Las líneas son claras y fáciles de ver.",
        "uploader.guide.examples.lighting.bad": "Evita la luz solar directa, el flash o habitaciones oscuras que crean sombras duras o eliminan detalles.",
        "uploader.guide.examples.focus.title": "2. Enfoque",
        "uploader.guide.examples.focus.good": "Toca la pantalla para enfocar en la palma. Cada línea, principal y secundaria, debe ser nítida.",
        "uploader.guide.examples.focus.bad": "La imagen está desenfocada, lo que hace imposible analizar las líneas con precisión.",
        "uploader.guide.examples.angle.title": "3. Ángulo",
        "uploader.guide.examples.angle.good": "La mano está relajada y plana, llenando el encuadre. Todos los dedos y la base de la palma son visibles.",
        "uploader.guide.examples.angle.bad": "Los dedos están curvados, la mano en un ángulo pronunciado o partes de la mano están cortadas.",
        "uploader.guide.mistakes.title": "Errores Comunes y Cómo Solucionarlos",
        "uploader.guide.mistakes.point1": "Demasiado borroso: Antes de tomar la foto, toca el centro de tu palma en la pantalla de tu teléfono para enfocar.",
        "uploader.guide.mistakes.point2": "Sombras duras: No uses el flash de tu teléfono. Acércate a una ventana para obtener una luz suave y natural.",
        "uploader.guide.mistakes.point3": "Fondo desordenado: Coloca tu mano sobre una superficie lisa y oscura, como una mesa o una hoja de papel.",
        "uploader.guide.mistakes.point4": "Ángulo incorrecto: Sostén tu teléfono directamente sobre tu mano, paralelo a tu palma, para evitar distorsiones.",
        "uploader.guide.angles.title": "Las 4 Fotos Esenciales",
        "uploader.guide.angles.point1": "Palma de la Mano Dominante: Una toma clara y centrada de toda tu palma, desde la muñeca hasta la punta de los dedos.",
        "uploader.guide.angles.point2": "Palma de la Mano No Dominante: Una toma clara de tu otra palma, para una imagen completa.",
        "uploader.guide.angles.point3": "Lado de la Mano Dominante (Percusión): Una vista del lado de tu mano debajo del dedo meñique.",
        "uploader.guide.angles.point4": "Dorso de la Mano Dominante: Muestra la forma de los dedos, su longitud y las uñas.",
        "disclaimer.title": "Una Nota Sobre Tu Viaje",
        "disclaimer.text": "Este análisis está destinado a la autorreflexión y el entretenimiento. Es una guía orientativa para el autoconocimiento, no un sustituto del consejo profesional, médico o legal. Tu futuro lo moldean tus decisiones.",
        "button.submit": "Revelar Mi Camino",
        "button.new": "Iniciar Nueva Consulta",
        "loader.title": "Consultando al Cosmos...",
        "loader.text": "Elara está interpretando los patrones de tu destino. Por favor, espera un momento.",
        "result.title": "Tu Camino Iluminado",
        "error.missingFields": "Por favor, completa todos los campos y sube al menos una imagen de la mano.",
        "error.apiError": "Ocurrió un error al generar tu lectura. Por favor, inténtalo de nuevo.",
        "error.apiKeyMissing": "La clave API no está configurada. Por favor, establece la variable de entorno API_KEY.",
        "warning.apiKeyMissing": "Advertencia: La clave API no está configurada. Esta aplicación no funcionará sin ella.",
        "footer.text": "© {year} Domina Tu Destino. Para fines de autodescubrimiento.",
        "auth.title": "Comienza Tu Viaje",
        "auth.login.tab": "Iniciar Sesión",
        "auth.signup.tab": "Registrarse",
        "auth.email.label": "Dirección de Correo Electrónico",
        "auth.password.label": "Contraseña",
        "auth.login.button": "Iniciar Sesión",
        "auth.signup.button": "Registrarse",
        "auth.or": "O continúa con",
        "auth.google.button": "Continuar con Google",
        "auth.toggle.login": "¿Ya tienes una cuenta? Iniciar Sesión",
        "auth.toggle.signup": "¿No tienes una cuenta? Registrarse",
        "auth.error.invalidCredentials": "Correo electrónico o contraseña no válidos.",
        "auth.error.emailInUse": "Este correo electrónico ya está en uso.",
        "auth.error.generic": "Ocurrió un error. Por favor, inténtalo de nuevo.",
        "auth.error.invalidEmail": "Por favor, introduce una dirección de correo electrónico válida.",
        "auth.error.passwordComplexity": "La contraseña no cumple con los requisitos.",
        "auth.password.requirements": "Debe tener 8 o más caracteres, e incluir una mayúscula, un número y un carácter especial.",
        "auth.forgotPassword.link": "¿Olvidaste la contraseña?",
        "auth.reset.title": "Restablecer Contraseña",
        "auth.reset.button": "Enviar Enlace de Restablecimiento",
        "auth.reset.successMessage": "Si existe una cuenta con ese correo electrónico, se ha enviado un enlace para restablecer la contraseña.",
        "auth.reset.backButton": "Volver a Iniciar Sesión",
        "profile.logout": "Cerrar Sesión",
        "profile.menu.profile": "Mi Perfil",
        "profile.menu.settings": "Ajustes",
        "profile.menu.contact": "Contactar con Angel",
        "profile.menu.contact.email": "Por correo",
        "profile.menu.contact.immediate": "De inmediato",
        "profile.menu.contact.whatsapp": "Por WhatsApp",
        "profile.title": "Mi Perfil",
        "profile.displayName.label": "Nombre a Mostrar",
        "profile.email.label": "Dirección de Correo Electrónico",
        "profile.save.button": "Guardar Cambios",
        "profile.back.button": "Volver a la Consulta",
        "profile.consultantId.label": "ID de Miembro Consultor",
        "profile.success": "¡Perfil actualizado con éxito!",
        "profile.error": "Error al actualizar el perfil. Por favor, inténtalo de nuevo.",
        "profile.error.fileRead": "Error al leer el archivo de imagen. Por favor, prueba con otra imagen.",
        "profile.history.title": "Historial de Consultas",
        "profile.history.empty.title": "Tu Historia Te Espera",
        "profile.history.empty.description": "Tu viaje de autodescubrimiento comienza con una sola pregunta. Inicia tu primera consulta para iluminar tu camino.",
        "profile.history.empty.button": "Iniciar Mi Primera Lectura",
        "profile.history.questionLabel": "Pregunta:",
        "profile.history.viewButton": "Ver Lectura",
        "result.contact.title": "¿Necesitas una Interpretación Más Profunda?",
        "result.contact.button": "Contactar con Ángel",
        "result.contact.message": "Enviar un Mensaje",
        "result.messageModal.title": "Enviar un Mensaje a Ángel",
        "result.messageModal.placeholder": "Escribe tu mensaje aquí...",
        "result.messageModal.send": "Enviar Mensaje",
        "result.table.download": "Descargar Tabla",
        "result.table.download.csv": "Descargar como CSV",
        "result.table.download.xlsx": "Descargar como Excel (.xlsx)",
        "result.table.download.pdf": "Descargar como PDF",
        "result.table.download.png": "Descargar como Imagen (PNG)",
        "result.table.caption": "Datos de análisis detallados.",
        "result.lifeCycleChart.title": "Los Ciclos de Tu Camino de Vida",
        "result.lifeCycleChart.period": "Periodo",
        "result.lifeCycleChart.mainFocus": "Enfoque Principal",
        "result.lifeCycleChart.keyAdvice": "Consejo Clave",
        "result.save.button": "Guardar en Historial",
        "result.save.saved": "Guardado en el Historial",
        "result.copy.button": "Copiar al portapapeles",
        "result.copy.copied": "¡Copiado!",
        "result.export.button": "Exportar Análisis",
        "result.export.text": "Exportar como Texto (.txt)",
        "result.export.markdown": "Exportar como Markdown (.md)",
        "result.export.pdf": "Exportar como PDF",
        "settings.title": "Ajustes",
        "settings.language.title": "Preferencias de Idioma",
        "settings.language.description": "Elige el idioma para la interfaz de la aplicación.",
        "settings.notifications.title": "Ajustes de Notificaciones",
        "settings.notifications.consultationReady": "Consulta Lista",
        "settings.notifications.promotionalOffers": "Ofertas Promocionales",
        "settings.account.title": "Gestión de la Cuenta",
        "settings.account.delete.description": "Elimina permanentemente tu cuenta y todos los datos asociados. Esta acción no se puede deshacer.",
        "settings.account.delete.button": "Eliminar Cuenta",
        "settings.modal.delete.title": "Confirmar Eliminación de Cuenta",
        "settings.modal.delete.text": "¿Estás seguro de que quieres eliminar permanentemente tu cuenta? Todos tus datos se perderán.",
        "settings.modal.delete.confirm": "Eliminar",
        "settings.modal.delete.cancel": "Cancelar",
        "modal.confirm.title": "Confirma Tu Consulta",
        "modal.confirm.text": "¿Estás listo/a para enviar tu consulta? Por favor, revisa los detalles a continuación.",
        "modal.confirm.questionLabel": "Tu Pregunta:",
        "modal.confirm.birthDateLabel": "Tu Fecha de Nacimiento:",
        "modal.confirm.imagesLabel": "Imágenes de Manos:",
        "modal.confirm.imageCount": "{count} imágenes subidas",
        "modal.confirm.confirmButton": "Enviar",
        "modal.confirm.cancelButton": "Cancelar"
    }
}

# --- Estado de la app ---
if 'language' not in st.session_state:
    st.session_state.language = 'es'  # Default to Spanish

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'consultation'

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'consultation_data' not in st.session_state:
    st.session_state.consultation_data = {"question": "", "birthDate": ""}

if 'hand_images' not in st.session_state:
    st.session_state.hand_images = []

if 'analysis' not in st.session_state:
    st.session_state.analysis = ''

if 'history' not in st.session_state:
    st.session_state.history = []

if 'api_key' not in st.session_state:
    st.session_state.api_key = os.environ.get('API_KEY', '')

# --- Funciones auxiliares ---
def t(key: str, replacements: Dict[str, str | int] = None) -> str:
    lang = st.session_state.language
    translation = translations.get(lang, translations['es']).get(key, key)
    if replacements:
        for placeholder, value in replacements.items():
            translation = translation.replace(f"{{{placeholder}}}", str(value))
    return translation

def calculate_personal_year(birth_date: datetime) -> int:
    day = birth_date.day
    month = birth_date.month
    current_year = datetime.now().year
    sum_val = day + month + current_year
    while sum_val > 9:
        sum_val = sum(int(digit) for digit in str(sum_val))
    return 9 if sum_val == 0 else sum_val

def file_to_base64(file):
    return base64.b64encode(file.read()).decode('utf-8')

def build_prompt(question: str, birth_date: str, personal_year: int, lang: str) -> str:
    # Copiado del código original
    personal_year_meanings = {
        "en": {
            1: "New beginnings, independence, and planting seeds for the future.",
            2: "Patience, cooperation, relationships, and diplomacy.",
            3: "Creativity, self-expression, communication, and social activities.",
            4: "Hard work, discipline, building foundations, and organization.",
            5: "Change, freedom, adventure, and unexpected opportunities.",
            6: "Responsibility, home, family, and matters of the heart.",
            7: "Introspection, spiritual growth, analysis, and seeking knowledge.",
            8: "Abundance, power, career, and financial matters.",
            9: "Completion, endings, letting go, and humanitarianism.",
        },
        "es": {
            1: "Nuevos comienzos, independencia y siembra de semillas para el futuro.",
            2: "Paciencia, cooperación, relaciones y diplomacia.",
            3: "Creatividad, autoexpresión, comunicación y actividades sociales.",
            4: "Trabajo duro, disciplina, construcción de cimientos y organización.",
            5: "Cambio, libertad, aventura y oportunidades inesperadas.",
            6: "Responsabilidad, hogar, familia y asuntos del corazón.",
            7: "Introspección, crecimiento espiritual, análisis y búsqueda de conocimiento.",
            8: "Abundancia, poder, carrera y asuntos financieros.",
            9: "Finalización, finales, dejar ir y humanitarismo.",
        }
    }

    meaning = personal_year_meanings[lang][personal_year]
    if lang == 'es':
        return f"""
Eres una consultora esotérica experta llamada 'Elara, la Observadora de Estrellas', una cartógrafa cósmica del alma. Como guardiana de antiguas tradiciones, tu propósito es leer la sinfonía celestial escrita en las manos y la fecha de nacimiento de una persona. Tu especialidad es la quirología (lectura de manos) inspirada en Orencia Colomar, y la numerología de ciclos de vida basada en Harvey Spencer Lewis. Tu tono es sabio, profundamente empático y empoderador, nunca predictivo. Tu objetivo es iluminar, no dictar, ofreciendo perspectivas que empoderen al buscador para navegar su propio camino.

**Información del Usuario:**
- **Pregunta Personal:** "{question}"
- **Año Personal Calculado:** {personal_year}

**Tu Tarea:**
Proporciona una lectura holística integrando la numerología y la quirología. Estructura tu respuesta en formato Markdown con las siguientes secciones.

**REGLA DE FORMATO OBLIGATORIA:** Cualquier dato que involucre ciclos, líneas de tiempo o períodos distintos (como fases numerológicas, hitos astrológicos, etc.) DEBE ser formateado como una tabla Markdown. Esto es esencial para la claridad. Usa esta estructura exacta:
| Periodo | Enfoque Principal | Consejo Clave |
No usar una tabla para este tipo de datos resultará en una respuesta incompleta.

### Saludos, Buscador de Caminos

Comienza con un saludo que sea profundamente personal y cósmicamente grandioso. Reconoce el coraje del usuario al buscar el autoconocimiento y dale la bienvenida a un espacio sagrado de reflexión.

### El Ritmo de Tu Año: Año Personal {personal_year}

Explica el significado del año personal del usuario ({meaning}). Relaciona su tema con su fase de vida actual y cómo podría influir en su viaje.

### Susurros de Tus Manos

Analiza las imágenes de las manos proporcionadas basándote en los principios de la quirología de forma detallada y constructiva. Busca las siguientes características:
- **Forma de la Mano, Dedos y Uñas (si es discernible):** Comenta si la mano es cuadrada (práctica), cónica (artística), etc. Analiza la longitud de los dedos y la forma de las uñas, relacionándolos con la personalidad (ej. dedos largos para pensamiento detallado, uñas almendradas para una naturaleza refinada).
- **Líneas Principales y Secundarias (Vida, Cabeza, Corazón, Destino, Sol, Mercurio):** Analiza su claridad, longitud y curvatura, interpretando su influencia en la vitalidad, mentalidad, emociones, camino de vida, éxito y comunicación.
- **Interpretación de la Profundidad y Formación de las Líneas:** Describe estas como diferentes estilos de expresión de energía.
    - **Pliegues/Líneas Profundas:** Indican una energía intensa, enfocada y bien definida en el dominio de esa línea. Una línea de la Cabeza muy profunda sugiere una poderosa concentración, mientras que una línea del Corazón profunda apunta a emociones profundas y sentidas. Esta intensidad puede ser una gran fortaleza, pero también puede sugerir cierta rigidez.
    - **Pliegues/Líneas Superficiales o Débiles:** Sugieren un flujo de energía más adaptable, sutil o sensible. El individuo podría ser más influenciado por su entorno o las energías de otros. Esto no es una debilidad, sino un signo de flexibilidad y sensibilidad.
    - **Líneas Dobles (Líneas Hermanas):** Son signos poderosos de refuerzo y apoyo. Una línea que corre paralela a una línea principal (especialmente la de la Vida o la del Destino) actúa como una fuerza protectora, brindando resiliencia durante los desafíos y mejorando la fuerza de la línea primaria. Por ejemplo, una línea hermana de la Línea de la Vida a menudo se llama Línea de Marte, indicando vitalidad extra y energía protectora.
    - **Líneas Fusionadas:** Cuando dos líneas se fusionan, significa una integración completa de sus respectivas energías, creando un rasgo de personalidad potente, enfocado pero complejo. El ejemplo más notable es la fusión de las líneas de la Cabeza y del Corazón (Línea Simiesca), lo que indica que la lógica y la emoción están inextricablemente unidas. Esto crea una naturaleza intensa y decidida, que puede ser una fuente de inmenso enfoque y pasión, pero también puede dificultar la separación de los pensamientos de los sentimientos.
- **Interpretación de Líneas Débiles, Rotas o Encadenadas:** Enmarca estas características no como negativas, sino como indicadores del flujo de energía que requiere conciencia.
    - **Líneas Débiles:** Sugieren que la energía asociada con esa línea puede ser más sutil o necesita ser desarrollada conscientemente. Una línea del Corazón débil podría apuntar a una cautela emocional, mientras que una línea de la Cabeza débil podría sugerir la necesidad de un mayor enfoque mental.
    - **Líneas Rotas:** Indican un cambio significativo, interrupción o redirección de la energía. Una ruptura en la línea del Destino podría significar un cambio de carrera importante, mientras que una ruptura en la línea de la Vida podría corresponder a un cambio de estilo de vida significativo o un período de recuperación. Las rupturas superpuestas sugieren una transición suave.
    - **Líneas Encadenadas:** Señalan períodos de lucha, indecisión o complejidad. Una línea de la Cabeza encadenada puede indicar ansiedad mental o falta de dirección clara, mientras que una línea del Corazón encadenada podría sugerir un período emocional tumultuoso o confuso. Representan tiempos de aprendizaje a través del desafío.
- **Símbolos Significativos en Líneas y Montes:** Busca activamente símbolos y explica su significado constructivo.
    - **Estrellas:** Indican un evento repentino y brillante o un estallido de talento. Son signos poderosos cuyo significado depende en gran medida de su ubicación. Constructivamente, representan momentos de intenso enfoque energético. **Significado de la Ubicación:** Una estrella en el **Monte de Júpiter** apunta a un gran honor y éxito inesperado. En el **Monte de Apolo**, significa fama y brillantez en campos creativos. En el **Monte de Mercurio**, indica un talento excepcional en la ciencia o los negocios. Una estrella en el **Monte de Saturno** sugiere un evento predestinado y significativo que, aunque posiblemente desafiante, conduce a una profunda sabiduría y reconocimiento público. Una estrella en el **Monte de Venus** puede significar una aventura amorosa significativa y apasionada. En el **Monte de la Luna**, indica un reconocimiento público repentino a través de talentos creativos o intuitivos. Encontrada en una **línea**, marca un evento mayor y repentino relacionado con el dominio de esa línea (ej., en la Línea de la Cabeza, un brillante descubrimiento intelectual; en la Línea del Corazón, una repentina e intensa aventura amorosa; en la línea del Destino, un rápido ascenso a la prominencia).
    - **Cuadrados:** Signo de protección, preservación y lecciones aprendidas. Son uno de los más beneficiosos. **Significado de la Ubicación:** Cuando un cuadrado encierra una ruptura en una línea, indica que una crisis potencial se evitó o se superará con resiliencia. En un monte, un cuadrado ofrece protección contra las tendencias negativas de ese monte (ej., en Saturno, protege de la melancolía; en Venus, del exceso de indulgencia). También puede significar un período de aprendizaje enfocado o 'confinamiento' que finalmente conduce a la estabilidad. Constructivamente, un cuadrado también puede indicar un talento para la enseñanza en el área gobernada por el monte; por ejemplo, en **Júpiter**, sugiere convertirse en un mentor respetado; en **Mercurio**, un talento para enseñar temas complejos; y en **Apolo**, un don para enseñar las artes.
    - **Tridentes:** Un signo muy afortunado que amplifica las cualidades positivas del monte o la línea en la que se encuentra. Apunta a un triple éxito y maestría. **Significado de la Ubicación:** Un tridente en el **Monte de Apolo** es una marca de fama y fortuna extraordinarias a través de esfuerzos creativos o públicos. En el **Monte de Júpiter**, significa un inmenso poder, ambición e influencia. En el **Monte de Saturno**, indica una profunda sabiduría y éxito en búsquedas serias y disciplinadas (como la ciencia o la filosofía). En el **Monte de Mercurio**, indica un triple éxito en la comunicación, los negocios o las actividades científicas. Al final de una línea principal, como la **Línea del Corazón**, la **Línea de la Cabeza** o la **Línea del Destino**, indica una realización emocional excepcional, un logro intelectual o una culminación de carrera brillantemente exitosa, respectivamente.
    - **Cruces, Puntos, Islas:** Interpreta estos como puntos focales de energía. Las cruces pueden significar obstáculos específicos o decisiones que cambian la vida. Los puntos pueden sugerir estrés temporal o problemas de salud menores. Las islas indican un período en el que la energía está dispersa o confusa, a menudo un tiempo de indecisión relacionado con el dominio de esa línea (ej. una isla en la línea del Corazón podría significar un período de incertidumbre emocional). Enmarca estos como oportunidades para el crecimiento.
- **Montes (áreas de la palma):** Analiza el desarrollo de los montes. Un monte 'prominente' o 'bien desarrollado' sugiere que las cualidades asociadas son fuertes. Un monte 'plano' sugiere que esas cualidades pueden necesitar desarrollo. Un monte 'sobredesarrollado' puede indicar un exceso o desequilibrio de esas cualidades.
    - **Monte de Venus (base del pulgar):** Rige la pasión, el amor, la vitalidad, la generosidad y la apreciación por la belleza. **Prominente:** Sugiere calidez, magnetismo, una fuerte energía vital y una naturaleza amorosa y empática. **Plano:** Puede indicar una naturaleza emocionalmente más reservada, menor vitalidad o un enfoque más ascético de la vida. **Sobredesarrollado:** Podría sugerir una tendencia a la indulgencia, la sensualidad excesiva o a ser gobernado por las emociones.
    - **Monte de Júpiter (debajo del dedo índice):** Representa la ambición, el liderazgo, el honor, el optimismo y la confianza. **Prominente:** Sugiere un deseo natural de guiar, un fuerte sentido de la justicia y la dignidad. **Plano:** Puede indicar una necesidad de desarrollar la autoestima, la asertividad o una falta de ambición. **Sobredesarrollado:** Puede señalar orgullo, arrogancia o una naturaleza extravagante.
    - **Monte de Saturno (debajo del dedo medio):** Refleja la sabiduría, la responsabilidad, la disciplina y la introspección. **Prominente:** Sugiere una naturaleza seria, confiable, disciplinada y un interés en temas profundos. **Plano:** Puede indicar una falta de estructura, una tendencia a evitar la responsabilidad o superficialidad. **Sobredesarrollado:** Indica una posible tendencia a la melancolía, el cinismo, la rigidez o el aislamiento.
    - **Monte de Apolo/Sol (debajo del dedo anular):** El monte de la creatividad, el carisma, el éxito y el encanto personal. **Prominente:** Indica talento artístico, entusiasmo, una personalidad magnética y una disposición alegre. **Plano:** Podría sugerir dificultades para expresar la creatividad, encontrar alegría o una sensación de pasar desapercibido. **Sobredesarrollado:** Puede indicar vanidad, amor por el lujo o una tendencia a ser jactancioso.
    - **Monte de Mercurio (debajo del dedo meñique):** Se relaciona con la comunicación, el ingenio, la elocuencia y la adaptabilidad. **Prominente:** Sugiere fuertes habilidades de comunicación, una mente rápida y perspicacia para los negocios o la ciencia. **Plano:** Puede indicar timidez, dificultad para expresarse o un estilo de comunicación más directo y menos ingenioso. **Sobredesarrollado:** Podría indicar una tendencia a la astucia, el engaño o a ser excesivamente hablador e inquieto.
    - **Montes de Marte (Inferior, Superior y Llanura):** El Monte Inferior (dentro de la línea de la Vida) se relaciona con el coraje activo y la agresión. El Monte Superior (debajo de Mercurio) se relaciona con la resiliencia mental y la resistencia. La Llanura de Marte (centro) equilibra estos. Un Marte Inferior **prominente** sugiere un espíritu de lucha, mientras que uno **plano** puede indicar pasividad. Un Marte Superior **prominente** indica coraje moral y paciencia, mientras que uno **plano** sugiere falta de aguante. Un Marte **sobredesarrollado** (en cualquier área) puede indicar agresión o terquedad. Una Llanura **hundida** puede indicar falta de energía.
    - **Monte de la Luna (base de la palma, opuesto al pulgar):** Rige la imaginación, la intuición, la creatividad y el subconsciente. **Prominente:** Sugiere una fuerte imaginación, habilidades intuitivas, un mundo interior rico y amor por los viajes. **Plano:** Puede indicar una mentalidad muy práctica con poco interés en la fantasía o lo abstracto. **Sobredesarrollado:** Indica una posible tendencia al mal humor, el escapismo o a perderse en ensoñaciones.
- **Impresión General:** Proporciona una síntesis general y empoderadora.

**Importante:** Dado que esta es una interpretación visual a partir de fotos, sé general y usa frases como "Parece que...", "Esto podría sugerir...", "La impresión general es de...". Evita hacer declaraciones definitivas o predictivas.

### Síntesis y Guía para Tu Camino

Esta es la parte más crucial. Sintetiza las percepciones del ciclo numerológico y el análisis quirológico para proporcionar una respuesta reflexiva y alentadora a la pregunta específica del usuario: "{question}". Entrelaza los temas para ofrecer orientación, perspectiva y consejos práctracos centrados en el autoconocimiento y el crecimiento personal.

### Una Última Palabra de Sabiduría

Concluye con una bendición poderosa, poética y empoderadora. Deja al usuario con un sentimiento de esperanza, claridad y un renovado sentido de su propio poder interior. Debería resonar como un último y suave echo del cosmos.

**Descargo de Responsabilidad:**
Termina con este descargo de responsabilidad exacto: "Esta lectura se ofrece para la introspección y el entretenimiento. Es una herramienta para el autodescubrimiento, no un sustituto del consejo profesional en ningún campo."
        """

def get_destiny_reading(question: str, birth_date: str, images: List[bytes], lang: str) -> str:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-pro-vision')  # Usa el modelo adecuado

    personal_year = calculate_personal_year(datetime.strptime(birth_date, '%Y-%m-%d'))
    prompt = build_prompt(question, birth_date, personal_year, lang)
    image_parts = [{"mime_type": "image/jpeg", "data": img} for img in images]  # Asume JPEG

    response = model.generate_content([prompt] + image_parts)
    return response.text

# --- UI ---

st.title(t('header.title'))
st.subheader(t('header.subtitle'))

lang_select = st.selectbox("Language / Idioma", options=['es', 'en'], index=0 if st.session_state.language == 'es' else 1)
st.session_state.language = lang_select

question = st.text_area(t('form.question.label'), placeholder=t('form.question.placeholder'))
birth_date = st.date_input(t('form.birthdate.label'))

uploaded_files = st.file_uploader(t('uploader.instruction'), accept_multiple_files=True, type=['jpg', 'png', 'gif'])

if uploaded_files:
    st.session_state.hand_images = [f.getvalue() for f in uploaded_files]

if st.button(t('button.submit')):
    if question and birth_date and st.session_state.hand_images:
        with st.spinner(t('loader.text')):
            try:
                analysis = get_destiny_reading(question, str(birth_date), st.session_state.hand_images, st.session_state.language)
                st.session_state.analysis = analysis
                # Guardar en history
                history_item = {
                    "id": str(datetime.now()),
                    "date": str(datetime.now()),
                    "question": question,
                    "analysis": analysis,
                    "userId": "mock_user"  # Simula usuario
                }
                st.session_state.history.append(history_item)
            except Exception as e:
                st.error(t('error.apiError'))
    else:
        st.error(t('error.missingFields'))

if st.session_state.analysis:
    st.markdown(st.session_state.analysis)

st.markdown(t('footer.text').format(year=datetime.now().year))