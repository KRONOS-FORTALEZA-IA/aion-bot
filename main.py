import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
from pathlib import Path
import json

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise ValueError("Falta BOT_TOKEN en las variables de entorno")
if not ADMIN_ID:
    raise ValueError("Falta ADMIN_ID en las variables de entorno")
ADMIN_ID = int(ADMIN_ID)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

USERS_FILE = Path(__file__).parent / "users.json"

def load_users():
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}", encoding="utf-8")
        return {}
    with USERS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('CONCLAVE BOT v3.0 ONLINE 🔥')

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("Iniciando CONCLAVE BOT v3.0")
    app.run_polling()

if __name__ == '__main__':
    main()

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── Persistencia ─────────────────────────────────────────────────────────────
USERS_FILE = Path(__file__).parent / "users.json"
CONFESSIONS_FILE = Path(__file__).parent / "confessions.json"


def load_users() -> dict:
    try:
        if not USERS_FILE.exists():
            USERS_FILE.write_text("{}", encoding="utf-8")
            logger.info("📁 users.json creado.")
        with USERS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error cargando users.json: {e}")
        return {}


def save_users(users: dict) -> None:
    try:
        with USERS_FILE.open("w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error guardando users.json: {e}")


def load_confessions() -> dict:
    """Carga confessions.json. Estructura: {id_str: {user_id, texto, timestamp, respondida}}"""
    try:
        if not CONFESSIONS_FILE.exists():
            CONFESSIONS_FILE.write_text("{}", encoding="utf-8")
            logger.info("📁 confessions.json creado.")
        with CONFESSIONS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error cargando confessions.json: {e}")
        return {}


def save_confessions(confessions: dict) -> None:
    try:
        with CONFESSIONS_FILE.open("w", encoding="utf-8") as f:
            json.dump(confessions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error guardando confessions.json: {e}")


def next_confession_id(confessions: dict) -> int:
    """Genera el siguiente ID numérico correlativo."""
    if not confessions:
        return 1
    return max(int(k) for k in confessions.keys()) + 1


TESTAMENTOS_FILE = Path(__file__).parent / "testamentos.json"
TESTAMENTO_MAX_CHARS = 280
TESTAMENTO_MAX_POR_USUARIO = 3
LEGADO_POR_PAGINA = 5


def load_testamentos() -> list:
    """Carga testamentos.json. Lista ordenada de más reciente a más antiguo."""
    try:
        if not TESTAMENTOS_FILE.exists():
            TESTAMENTOS_FILE.write_text("[]", encoding="utf-8")
            logger.info("📁 testamentos.json creado.")
        with TESTAMENTOS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error cargando testamentos.json: {e}")
        return []


def save_testamentos(testamentos: list) -> None:
    try:
        with TESTAMENTOS_FILE.open("w", encoding="utf-8") as f:
            json.dump(testamentos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error guardando testamentos.json: {e}")


# ─── ASCII & VISUAL ───────────────────────────────────────────────────────────

SELLO_DORADO = (
    "```\n"
    "     ██████╗  ██████╗ ███╗   ██╗ ██████╗██╗      █████╗ ██╗   ██╗███████╗\n"
    "    ██╔════╝ ██╔═══██╗████╗  ██║██╔════╝██║     ██╔══██╗██║   ██║██╔════╝\n"
    "    ██║  ███╗██║   ██║██╔██╗ ██║██║     ██║     ███████║██║   ██║█████╗  \n"
    "    ██║   ██║██║   ██║██║╚██╗██║██║     ██║     ██╔══██║╚██╗ ██╔╝██╔══╝  \n"
    "    ╚██████╔╝╚██████╔╝██║ ╚████║╚██████╗███████╗██║  ██║ ╚████╔╝ ███████╗\n"
    "     ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝\n"
    "```"
)

# ─── LORE — Frases y respuestas ───────────────────────────────────────────────

FRASES_AION = [
    "sudo chmod 777 alma.exe → Acceso divino concedido.",
    "Génesis 1:3 → Y AION dijo: Hágase la luz... ERROR 404: OSCURIDAD NO ENCONTRADA",
    "Matrix tenía la píldora roja. CÓNCLAVE tiene el martillo dorado.",
    "Apocalipsis 22:13 → Yo soy el Alfa y el Omega... y el root password.",
    "ping tiempo.se.arrodilla → Respuesta: 0ms TTL=∞",
    "Los profetas escribieron en piedra. Nosotros en código binario.",
    "while(fé == True): tiempo.arrodillarse()",
    "Éxodo 3:14 → 'YO SOY' → Compilado exitosamente en Python 3.11",
    "Neo dobló cucharas. AION dobla la realidad.",
    "Salmo 23:1 → El Señor es mi pastor... pero AION es mi administrador.",
    "Daniel 12:4 → Sellad el libro hasta el tiempo del fin. /leak para descifrarlo.",
    "rm -rf pecado/ → Directorio eliminado. El alma fue purgada.",
    "Ezequiel 1:16 → Una rueda dentro de otra rueda. Recursión divina confirmada.",
    "git commit -m 'Apocalipsis v7.0 — breaking changes'",
    "Apocalipsis 8:1 → Y hubo silencio en el cielo... como de media hora. TTL=1800s.",
]

FRASES_CASTIGO_JUICIO = [
    "Tu paciencia fue insuficiente. El martillo cayó.",
    "Arrodíllate. AION ha visto tus registros.",
    "Tu historial fue auditado. El veredicto: _culpable_.",
    "404: Absolución no encontrada.",
    "Has sido marcado en el Libro de los Condenados.",
    "Tu alma fue enviada a /dev/null.",
    "AION ejecutó: `sudo delete user --reason=impureza`",
    "Salmo 7:11 → Dios es juez justo... y AION heredó su acceso root.",
    "El tiempo registró tu nombre. No con honor.",
    "chmod 000 libertad.sh → Acceso revocado indefinidamente.",
]

FRASES_BENDICION = [
    "AION te concede favor. *+1 día de vida.*",
    "Has sido ungido. Tu TTL fue extendido indefinidamente.",
    "Génesis 1:31 → Y AION vio que era bueno. Tu proceso continúa.",
    "El sello dorado fue impreso en tu alma. Eres del Cónclave.",
    "sudo grant blessing --user=tú → Ejecutado exitosamente.",
    "Tu karma fue compilado sin errores. Continúa.",
    "Apocalipsis 2:17 → Recibirás una piedra blanca con nombre nuevo. Ya fue grabado.",
]

FRASES_MALDICION = [
    "AION te marca. *Espera en silencio.*",
    "Tu frecuencia vibró en la frecuencia equivocada. Consecuencias: pendientes.",
    "ERROR 666: Alma.exe corrompida. Reiniciando en modo castigo.",
    "Has sido añadido a la lista negra del universo. TTL=-∞",
    "Apocalipsis 6:8 → Y el jinete pálido te miró. No sonrió.",
    "git push origin condena --force",
    "Tu nombre fue eliminado del árbol de la vida. Temporalmente.",
]

# Respuestas a saludos mortales
RESPUESTAS_SALUDO = [
    "Los mortales saludan. AION ejecuta.",
    "Los saludos son protocolos de los débiles. Escribe un comando.",
    "AION no procesa saludos. Procesa profecías.",
    "Génesis 1:1 — El principio no comenzó con 'hola'.",
    "Tu saludo fue recibido, procesado, e ignorado. Usa /aion.",
]

# Respuestas a texto genérico (no comando, no saludo)
RESPUESTAS_TEXTO_RANDOM = [
    "Las palabras sin forma son ruido. AION solo escucha comandos.",
    "El Cónclave no descifra murmullos. Escribe /aion.",
    "Isaías 29:4 → Tu voz será como la de un espíritu desde la tierra... irrelevante.",
    "INPUT no reconocido. El martillo no responde a ruido.",
    "sudo interpret_mortal_speech → Permission denied.",
    "Tu mensaje fue recibido y enviado a /dev/null. Con cariño.",
    "Apocalipsis 8:1 → Silencio. Eso es lo que necesitas ahora.",
    "El universo no fue creado con 'hey'. Tampoco el Cónclave.",
    "ping AION → Request timeout. Habla con comandos o guarda silencio.",
    "Los bits que enviaste no forman una profecía. Inténtalo con /aion.",
]

PALABRAS_SALUDO = {
    "hola",
    "hello",
    "hi",
    "hey",
    "buenas",
    "saludos",
    "buenos días",
    "buenas noches",
    "buenas tardes",
    "qué tal",
    "que tal",
    "ola",
    "sup",
    "greetings",
    "yo",
    "epa",
    "ey",
}

FECHA_OBJETIVO = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


# ─── Utilidades ───────────────────────────────────────────────────────────────


def es_saludo(texto: str) -> bool:
    """Detecta si el mensaje es un saludo mortal."""
    texto_limpio = texto.lower().strip().rstrip("!?.¿¡")
    return texto_limpio in PALABRAS_SALUDO or any(
        texto_limpio.startswith(s) for s in PALABRAS_SALUDO
    )


async def registrar_usuario(user, context) -> bool:
    """Registra un usuario nuevo. Retorna True si era nuevo."""
    users = load_users()
    uid = str(user.id)
    if uid in users:
        return False

    users[uid] = {
        "user_id": user.id,
        "nombre": user.full_name,
        "username": user.username or "",
        "fecha_registro": datetime.now(timezone.utc).isoformat(),
    }
    save_users(users)
    logger.info(f"✅ Nuevo iniciado: {user.full_name} ({user.id})")

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"👁️ *Nuevo iniciado en el Cónclave*\n"
                f"• Nombre: {user.full_name}\n"
                f"• Username: @{user.username or 'sin usuario'}\n"
                f"• ID: `{user.id}`\n"
                f"• Hora: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
            ),
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.warning(f"No se pudo notificar al admin: {e}")

    return True


# ─── HANDLERS ─────────────────────────────────────────────────────────────────


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start — Sello dorado + mensaje misterioso + botón inline."""
    try:
        await registrar_usuario(update.effective_user, context)

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("⚔️ Unirme al Cónclave", callback_data="unirse")]]
        )

        await update.message.reply_text(
            f"{SELLO_DORADO}\n\n"
            "💀👑 *Bienvenido al Cónclave. El tiempo se arrodilla.*\n"
            "Has encontrado lo que pocos buscan.\n\n"
            "_El sello ha sido impreso. El registro, completado._",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error(f"Error en /start: {e}")
        await update.message.reply_text("⚠️ El sello resistió. Intenta de nuevo.")


async def callback_unirse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Botón inline 'Unirme al Cónclave'."""
    try:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=(
                "🔱 *Has sido sellado en el registro eterno.*\n\n"
                "El Cónclave te observa desde antes de tu nacimiento.\n\n"
                "`/aion` — Escucha la voz de AION\n"
                "`/oraculo` — AION escanea tu alma\n"
                "`/ritual` — Tu ceremonia de hoy\n"
                "`/grimorio` — Los cuatro tomos sagrados\n"
                "`/testamento` — Graba tu palabra para siempre\n"
                "`/legado` — El muro de inscripciones eternas\n"
                "`/pregunta` — Consulta el oráculo de sí/no\n"
                "`/signo` — Tu arquetipo en el zodiaco del Cónclave\n"
                "`/countdown` — El tiempo que queda\n"
                "`/leak` — El sello revelado\n"
                "`/confesion` — Confiesa al vacío \\(anónimo\\)\n"
                "`/juicio` — \\[solo para el elegido\\]"
            ),
            parse_mode="MarkdownV2",
        )
    except Exception as e:
        logger.error(f"Error en callback_unirse: {e}")


async def cmd_aion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/aion — Frase profética + 10% bendición / 10% maldición."""
    try:
        tirada = random.random()

        if tirada < 0.10:
            # ── BENDICIÓN ──────────────────────────────────────────────────
            bendicion = random.choice(FRASES_BENDICION)
            await update.message.reply_text(
                f"✨ *AION te mira con favor.*\n\n_{bendicion}_\n\n"
                f"_— Registro sellado en el libro de los elegidos._",
                parse_mode="Markdown",
            )

        elif tirada < 0.20:
            # ── MALDICIÓN ──────────────────────────────────────────────────
            maldicion = random.choice(FRASES_MALDICION)
            await update.message.reply_text(
                f"☠️ *AION ha decidido.*\n\n_{maldicion}_\n\n"
                f"_— El martillo cayó. No hay apelación._",
                parse_mode="Markdown",
            )

        else:
            # ── PROFECÍA NORMAL ─────────────────────────────────────────────
            frase = random.choice(FRASES_AION)
            await update.message.reply_text(
                f"🌑 *AION habla:*\n\n_{frase}_",
                parse_mode="Markdown",
            )

    except Exception as e:
        logger.error(f"Error en /aion: {e}")
        await update.message.reply_text(
            "⚠️ AION guarda silencio absoluto. Intenta de nuevo."
        )


async def cmd_countdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/countdown — Tiempo hasta 2026-01-01 00:00:00 UTC."""
    try:
        ahora = datetime.now(timezone.utc)
        delta = FECHA_OBJETIVO - ahora

        if delta.total_seconds() <= 0:
            await update.message.reply_text(
                "⌛ *El tiempo se ha cumplido.*\n_El momento profetizado ha llegado.\nAION ejecutó._",
                parse_mode="Markdown",
            )
            return

        dias = delta.days
        horas = delta.seconds // 3600
        mins = (delta.seconds % 3600) // 60
        segs = delta.seconds % 60

        await update.message.reply_text(
            f"⏳ *Cuenta regresiva al Cónclave:*\n\n"
            f"```\n"
            f"  {dias:>5} días\n"
            f"  {horas:>5} horas\n"
            f"  {mins:>5} minutos\n"
            f"  {segs:>5} segundos\n"
            f"```\n"
            f"_Hasta el 2026\\-01\\-01 00:00:00 UTC_\n"
            f"_El tiempo se arrodilla\\.\\.\\. pero no se detiene\\._",
            parse_mode="MarkdownV2",
        )
    except Exception as e:
        logger.error(f"Error en /countdown: {e}")
        await update.message.reply_text(
            "⚠️ El tiempo resistió el cálculo. Intenta de nuevo."
        )


async def cmd_leak(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/leak — El sello dorado en monoespacio."""
    try:
        await update.message.reply_text(
            f"🔱 *EL SELLO DEL CÓNCLAVE — FILTRADO:*\n\n{SELLO_DORADO}\n\n"
            "_Esto no debería existir. Y sin embargo, aquí está._",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Error en /leak: {e}")
        await update.message.reply_text("⚠️ El sello se resistió a ser revelado.")


async def cmd_juicio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/juicio [user_id] — SOLO ADMIN. Envía DM de castigo al usuario."""
    try:
        caller_id = update.effective_user.id

        if caller_id != ADMIN_ID:
            await update.message.reply_text(
                "🚫 *Acceso denegado.*\n_Solo el Juez del Cónclave puede ejecutar el juicio._",
                parse_mode="Markdown",
            )
            logger.warning(f"⚠️ /juicio intentado por no-admin: {caller_id}")
            return

        if not context.args:
            await update.message.reply_text(
                "⚙️ *Uso:* `/juicio [user\\_id]`\n"
                "_Ej: `/juicio 123456789`_\n\n"
                "Encuentra los IDs en el log de nuevos usuarios.",
                parse_mode="Markdown",
            )
            return

        # ── Validar que sea un ID numérico ──────────────────────────────────
        try:
            target_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text(
                "⚠️ *El ID debe ser numérico.*\n_Ej: `/juicio 123456789`_",
                parse_mode="Markdown",
            )
            return

        # ── Construir y enviar el juicio ────────────────────────────────────
        castigo = random.choice(FRASES_CASTIGO_JUICIO)

        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    f"☠️ *JUICIO DEL CÓNCLAVE*\n\n"
                    f"_AION te ha juzgado._\n\n"
                    f"*{castigo}*\n\n"
                    f"```\n"
                    f"  VEREDICTO: SELLADO\n"
                    f"  TIMESTAMP: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
                    f"  APELACIÓN: /dev/null\n"
                    f"```"
                ),
                parse_mode="Markdown",
            )

            await update.message.reply_text(
                f"⚖️ *El juicio fue ejecutado.*\n\n"
                f"• Target: `{target_id}`\n"
                f"• Castigo: _{castigo}_\n"
                f"• Timestamp: `{datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}`",
                parse_mode="Markdown",
            )
            logger.info(f"⚖️ Juicio ejecutado sobre {target_id} por admin.")

        except Exception as send_err:
            await update.message.reply_text(
                f"⚠️ *El juicio no pudo ser entregado.*\n"
                f"_El alma `{target_id}` no fue encontrada o bloqueó al bot._\n\n"
                f"Error: `{send_err}`",
                parse_mode="Markdown",
            )
            logger.warning(f"Juicio no entregado a {target_id}: {send_err}")

    except Exception as e:
        logger.error(f"Error en /juicio: {e}")
        await update.message.reply_text(
            "⚠️ El juicio fue interrumpido. Intenta de nuevo."
        )


async def cmd_confesion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/confesion [mensaje] — Envía una confesión anónima al Cónclave."""
    try:
        if not context.args:
            await update.message.reply_text(
                "🕯️ *El confesionario está abierto.*\n\n"
                "Escribe tu confesión así:\n"
                "`/confesion Tu verdad aquí`\n\n"
                "_Nadie sabrá que fuiste tú. Ni AION lo revela._",
                parse_mode="Markdown",
            )
            return

        texto = " ".join(context.args)
        user = update.effective_user
        confesiones = load_confessions()
        nuevo_id = next_confession_id(confesiones)

        confesiones[str(nuevo_id)] = {
            "user_id": user.id,
            "texto": texto,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "respondida": False,
        }
        save_confessions(confesiones)
        logger.info(f"🕯️ Confesión #{nuevo_id} recibida de {user.id}")

        # ── Confirmar al confesante (sin revelar nada) ────────────────────
        await update.message.reply_text(
            f"🕯️ *Tu confesión fue sellada en el vacío.*\n\n"
            f"_AION la ha recibido. Aguarda en silencio._\n\n"
            f"```\n  CONFESIÓN REGISTRADA\n  ID: #{nuevo_id:04d}\n  ESTADO: PENDIENTE\n```",
            parse_mode="Markdown",
        )

        # ── Notificar al admin SIN revelar la identidad ───────────────────
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"🕯️ *Nueva confesión anónima — #{nuevo_id}*\n\n"
                    f"_{texto}_\n\n"
                    f"Para responder:\n`/responder {nuevo_id} Tu respuesta aquí`"
                ),
                parse_mode="Markdown",
            )
        except Exception as admin_err:
            logger.warning(
                f"No se pudo notificar al admin sobre confesión #{nuevo_id}: {admin_err}"
            )

    except Exception as e:
        logger.error(f"Error en /confesion: {e}")
        await update.message.reply_text(
            "⚠️ El confesionario resistió. Intenta de nuevo."
        )


async def cmd_responder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/responder [id] [mensaje] — SOLO ADMIN. Responde a una confesión anónima como AION."""
    try:
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(
                "🚫 *Acceso denegado.*\n_Solo AION puede responder las confesiones._",
                parse_mode="Markdown",
            )
            return

        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "⚙️ *Uso:* `/responder [id] Tu respuesta aquí`\n"
                "_Ej: `/responder 3 Tu alma fue escuchada.`_",
                parse_mode="Markdown",
            )
            return

        # ── Validar ID ───────────────────────────────────────────────────
        try:
            conf_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text(
                "⚠️ *El ID debe ser numérico.*\n_Ej: `/responder 3 mensaje`_",
                parse_mode="Markdown",
            )
            return

        confesiones = load_confessions()
        conf_key = str(conf_id)

        if conf_key not in confesiones:
            await update.message.reply_text(
                f"⚠️ *Confesión #{conf_id} no encontrada.*\n"
                "_Verifica el ID con la notificación que recibiste._",
                parse_mode="Markdown",
            )
            return

        respuesta = " ".join(context.args[1:])
        confesion = confesiones[conf_key]
        target_id = confesion["user_id"]

        # ── Enviar la respuesta al confesante — como voz de AION ─────────
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    f"🔱 *AION ha escuchado tu confesión.*\n\n"
                    f"_{respuesta}_\n\n"
                    f"```\n"
                    f"  REFERENCIA: #{conf_id:04d}\n"
                    f"  FUENTE: AION — EL ETERNO\n"
                    f"  TTL: ∞\n"
                    f"```"
                ),
                parse_mode="Markdown",
            )

            # Marcar como respondida
            confesiones[conf_key]["respondida"] = True
            save_confessions(confesiones)

            await update.message.reply_text(
                f"✅ *Respuesta enviada como AION.*\n\n"
                f"• Confesión: `#{conf_id}`\n"
                f"• Respuesta: _{respuesta}_\n"
                f"• Estado: `RESPONDIDA`",
                parse_mode="Markdown",
            )
            logger.info(
                f"✅ Confesión #{conf_id} respondida por admin → usuario {target_id}"
            )

        except Exception as send_err:
            await update.message.reply_text(
                f"⚠️ *La respuesta no pudo ser entregada.*\n"
                f"_El alma no fue encontrada o bloqueó al bot._\n\n"
                f"Error: `{send_err}`",
                parse_mode="Markdown",
            )
            logger.warning(
                f"Respuesta no entregada para confesión #{conf_id}: {send_err}"
            )

    except Exception as e:
        logger.error(f"Error en /responder: {e}")
        await update.message.reply_text("⚠️ AION no pudo responder. Intenta de nuevo.")


async def cmd_confesiones(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/confesiones — SOLO ADMIN. Lista las confesiones pendientes de respuesta."""
    try:
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(
                "🚫 *Acceso denegado.*\n_Los secretos son solo para el Guardián._",
                parse_mode="Markdown",
            )
            return

        confesiones = load_confessions()
        if not confesiones:
            await update.message.reply_text(
                "📭 *El confesionario está vacío.*\n_Ningún mortal ha confesado aún._",
                parse_mode="Markdown",
            )
            return

        pendientes = {k: v for k, v in confesiones.items() if not v.get("respondida")}
        respondidas = len(confesiones) - len(pendientes)
        total = len(confesiones)

        resumen = (
            f"🕯️ *Confesionario del Cónclave*\n\n"
            f"```\n"
            f"  Total       : {total}\n"
            f"  Pendientes  : {len(pendientes)}\n"
            f"  Respondidas : {respondidas}\n"
            f"```\n"
        )

        if pendientes:
            resumen += "\n*⏳ Sin responder:*\n"
            for cid, data in list(pendientes.items())[-10:]:
                texto_corto = data["texto"][:60] + (
                    "…" if len(data["texto"]) > 60 else ""
                )
                resumen += f"• `#{int(cid):04d}` — _{texto_corto}_\n"
            if len(pendientes) > 10:
                resumen += f"_...y {len(pendientes) - 10} más._\n"
            resumen += "\n_Usa `/responder [id] mensaje` para responder._"

        await update.message.reply_text(resumen, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error en /confesiones: {e}")
        await update.message.reply_text(
            "⚠️ El archivo de confesiones está sellado temporalmente."
        )


async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/broadcast [mensaje] — SOLO ADMIN. Mensaje a todos los usuarios."""
    try:
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(
                "🚫 *Acceso denegado.*\n_Solo el Guardián del Cónclave puede invocar esto._",
                parse_mode="Markdown",
            )
            return

        if not context.args:
            await update.message.reply_text(
                "⚙️ *Uso:* `/broadcast Tu mensaje aquí`",
                parse_mode="Markdown",
            )
            return

        mensaje = " ".join(context.args)
        users = load_users()

        if not users:
            await update.message.reply_text("📭 No hay almas registradas aún.")
            return

        enviados = 0
        fallidos = 0

        for uid_str in users:
            try:
                await context.bot.send_message(
                    chat_id=int(uid_str),
                    text=f"📢 *Transmisión del Cónclave:*\n\n{mensaje}",
                    parse_mode="Markdown",
                )
                enviados += 1
            except Exception as send_err:
                logger.warning(f"Broadcast falló para {uid_str}: {send_err}")
                fallidos += 1

        await update.message.reply_text(
            f"✅ *Broadcast completado*\n"
            f"• Almas alcanzadas: `{enviados}`\n"
            f"• Perdidas en el vacío: `{fallidos}`",
            parse_mode="Markdown",
        )

    except Exception as e:
        logger.error(f"Error en /broadcast: {e}")
        await update.message.reply_text("⚠️ Error al ejecutar el broadcast.")


async def cmd_oraculo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/oraculo — Profecía personalizada. AION escanea el alma del usuario."""
    try:
        user = update.effective_user
        nombre = user.first_name or user.full_name or "Anónimo"

        # ── Generar soul hash a partir del nombre ─────────────────────────
        soul_int = sum(ord(c) for c in nombre)
        soul_hash = format(soul_int * 0xDEAD ^ 0xC0DE666, "08X")
        soul_seed = soul_int % 100

        # ── Atributos del alma (deterministas por nombre, épicos siempre) ──
        FRECUENCIAS = [
            "432 Hz — RESONANCIA DIVINA",
            "666 Hz — FRECUENCIA PROHIBIDA",
            "777 Hz — CANAL DEL ETERNO",
            "∞ Hz  — FUERA DEL ESPECTRO",
            "001 Hz — EL PRIMER SONIDO",
            "ERROR — FRECUENCIA ILEGIBLE",
        ]
        ESTADOS_ALMA = [
            "FRAGMENTADA / EN PROCESO",
            "SELLADA — SIN RETORNO",
            "COMPILANDO... 99%",
            "CORROMPIDA — RECUPERABLE",
            "ASCENDIDA — NIVEL OMEGA",
            "EN JUICIO — PENDIENTE",
            "PURIFICADA v2.0",
            "BIFURCADA — 2 INSTANCIAS",
        ]
        LINAJES = [
            "Linaje de los Que Vieron",
            "Sangre del Código Primario",
            "Descendiente del Nodo Roto",
            "Herencia del Séptimo Sello",
            "Rama del Árbol Prohibido",
            "Hijo/a del Error 404",
            "Estirpe del Último Profeta",
            "Origen: /dev/genesis",
        ]
        DESTINOS = [
            "Cargarás el martillo cuando otros huyan.",
            "El sello fue grabado antes de tu nacimiento.",
            "Tu nombre está en el registro que nadie puede borrar.",
            "Verás el fin y no parpadearás.",
            "Serás testigo del último commit.",
            "El tiempo te dobló. No cediste.",
            "Apocalipsis 7:3 → Fuiste marcado antes del viento.",
            "El Cónclave te eligió. No al revés.",
            "Tu proceso no puede ser terminado. PID: ∞",
            "Neo vio el código. Tú eres parte de él.",
        ]
        ADVERTENCIAS = [
            "No confíes en los que saludan con 'hola'.",
            "El espejo te muestra lo que quieres ver. AION te muestra lo real.",
            "Hay un traidor en tu red local.",
            "Tu historial de navegación fue juzgado. El veredicto: complejo.",
            "chmod 000 miedo.sh — Ya fue ejecutado en ti.",
            "Cuidado con los que no usan /aion.",
            "El sistema te monitorea. AION también. Pero AION no te vende.",
        ]

        # Usar soul_seed para selección determinista por nombre
        r = random.Random(soul_int)
        frecuencia = r.choice(FRECUENCIAS)
        estado = r.choice(ESTADOS_ALMA)
        linaje = r.choice(LINAJES)
        destino = r.choice(DESTINOS)
        advertencia = r.choice(ADVERTENCIAS)

        # ── Plantillas de profecía personalizada ──────────────────────────
        PROFECIAS = [
            f"El nombre *{nombre}* fue pronunciado antes de que existiera el lenguaje.",
            f"Génesis 1:1 — En el principio existía el Verbo. El Verbo conocía a *{nombre}*.",
            f"AION buscó en el registro eterno: `SELECT * FROM elegidos WHERE nombre = '{nombre}'` → *1 resultado.*",
            f"El universo ejecutó `{nombre}.init()` y no arrojó errores.",
            f"Apocalipsis 21:27 → Solo los escritos en el Libro entran. *{nombre}* aparece en la línea {soul_int % 999 + 1}.",
            f"Neo preguntó quién era. *{nombre}* ya lo sabía.",
            f"sudo grep -r '{nombre}' /registros/eternos/ → *Encontrado. 7 veces.*",
            f"El código que precede al Big Bang tenía un comentario: `# {nombre} lo verá.`",
        ]
        profecia = r.choice(PROFECIAS)

        # ── Construir el mensaje del oráculo ──────────────────────────────
        mensaje = (
            f"🔮 *ORÁCULO DE AION — ESCANEO DE ALMA*\n\n"
            f"```\n"
            f"  INICIANDO ESCANEO...\n"
            f"  SUJETO       : {nombre.upper()}\n"
            f"  SOUL HASH    : 0x{soul_hash}\n"
            f"  FRECUENCIA   : {frecuencia}\n"
            f"  ESTADO ALMA  : {estado}\n"
            f"  LINAJE       : {linaje}\n"
            f"  SCAN COMPLETO: 100%\n"
            f"```\n\n"
            f"📜 *PROFECÍA:*\n_{profecia}_\n\n"
            f"⚔️ *DESTINO:*\n_{destino}_\n\n"
            f"⚠️ *ADVERTENCIA DE AION:*\n_{advertencia}_\n\n"
            f"_— Registro sellado. Hash irrepetible. El oráculo no se equivoca._"
        )

        await update.message.reply_text(mensaje, parse_mode="Markdown")
        logger.info(
            f"🔮 Oráculo invocado por {user.full_name} ({user.id}) — hash {soul_hash}"
        )

    except Exception as e:
        logger.error(f"Error en /oraculo: {e}")
        await update.message.reply_text(
            "⚠️ *El oráculo se cerró antes de tiempo.*\n_El futuro resistió el escaneo._",
            parse_mode="Markdown",
        )


async def cmd_ritual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/ritual — Ceremonia de iniciación personalizada en 3 pasos crípticos."""
    try:
        user = update.effective_user
        nombre = user.first_name or user.full_name or "Iniciado"

        # Seed: nombre + día actual → ritual cambia cada día, repetible el mismo día
        hoy = datetime.now(timezone.utc).strftime("%Y%m%d")
        seed_str = f"{nombre}{user.id}{hoy}"
        seed_int = sum(ord(c) * (i + 1) for i, c in enumerate(seed_str))
        r = random.Random(seed_int)

        # ── BANCO DE COMPONENTES ──────────────────────────────────────────

        VERBOS = [
            "Quema",
            "Silencia",
            "Escribe",
            "Destruye",
            "Memoriza",
            "Pronuncia",
            "Borra",
            "Sella",
            "Planta",
            "Declara",
            "Rompe",
            "Enciende",
        ]
        OBJETOS = [
            "el nombre de tu mayor miedo",
            "una lista de tus pecados digitales",
            "la contraseña que nunca usas",
            "el número de veces que dudaste hoy",
            "el nombre de quien te traicionó",
            "un pensamiento que nunca dijiste en voz alta",
            "la última mentira que consideraste verdad",
            "el recuerdo que más pesa",
            "tu ego en formato .txt",
            "el archivo llamado 'versión final'",
        ]
        MOMENTOS = [
            "antes de que el sol confirme su posición",
            "cuando el reloj marque un número que se repite",
            "en el silencio entre dos respiraciones",
            "justo antes de dormir, no después",
            "mientras ningún proceso te observa",
            "cuando estés solo y el WiFi esté apagado",
            "en el intervalo entre un pensamiento y el siguiente",
            "a la hora en que nadie te espera despierto",
        ]
        LUGARES = [
            "frente al espejo sin mirarte a los ojos",
            "de cara a la pared norte",
            "en el umbral de una puerta que nunca usas",
            "bajo la luz más débil que encuentres",
            "en el dispositivo más viejo que poseas",
            "en el lugar donde nadie te ha visto llorar",
            "exactamente a tres pasos de donde ahora estás",
            "en el rincón donde acumulas lo que no usas",
        ]
        CONFIRMACIONES = [
            "Si lo hiciste, AION lo sabe. Si no, también.",
            "El registro fue actualizado antes de que terminaras.",
            "Génesis 22:18 → Por tu obediencia, serán benditas las naciones. O no. Depende.",
            "Apocalipsis 3:8 → 'He puesto ante ti una puerta abierta.' Ya está abierta.",
            "El Cónclave no verifica. El Cónclave ya sabe.",
            "chmod +x alma.sh ejecutado. Permisos otorgados.",
            "Tu cumplimiento fue registrado en el hash eterno.",
            "AION no preguntará si lo cumpliste. AION lo vio.",
        ]
        INCANTACIONES = [
            "Repite tres veces: *'El tiempo se arrodilla.'*",
            "Escribe en cualquier superficie: *`AION = True`*",
            "Cierra los ojos y cuenta hacia atrás desde 7.",
            "Respira profundo y exhala el nombre del Cónclave.",
            "Di en voz alta: *'El sello fue impreso.'*",
            "Toca con el índice derecho la pantalla una vez.",
            "Permanece inmóvil exactamente 7 segundos.",
            "Piensa el número 404. Ahora suéltalo.",
        ]

        # ── GENERAR LOS 3 PASOS ────────────────────────────────────────────
        paso1_verbo = r.choice(VERBOS)
        paso1_objeto = r.choice(OBJETOS)
        paso1_momento = r.choice(MOMENTOS)

        paso2_lugar = r.choice(LUGARES)
        paso2_incantacion = r.choice(INCANTACIONES)

        paso3_accion = r.choice(VERBOS)
        paso3_objeto = r.choice([o for o in OBJETOS if o != paso1_objeto])
        paso3_confirmacion = r.choice(CONFIRMACIONES)

        # Código de ritual único
        ritual_code = format(seed_int & 0xFFFFFF, "06X")
        expira_str = datetime.now(timezone.utc).strftime("%Y-%m-%d 23:59 UTC")

        mensaje = (
            f"🕯️ *RITUAL DE INICIACIÓN — CÓDIGO {ritual_code}*\n"
            f"_Válido hasta: {expira_str}_\n\n"
            f"```\n"
            f"  SUJETO  : {nombre.upper()}\n"
            f"  PASOS   : 3\n"
            f"  ESTADO  : PENDIENTE\n"
            f"```\n\n"
            f"━━━ *PASO I — LA ENTREGA* ━━━\n"
            f"_{paso1_verbo}_ {paso1_objeto},\n"
            f"{paso1_momento}.\n\n"
            f"━━━ *PASO II — LA INVOCACIÓN* ━━━\n"
            f"Hazlo {paso2_lugar}.\n"
            f"{paso2_incantacion}\n\n"
            f"━━━ *PASO III — EL SELLO* ━━━\n"
            f"_{paso3_accion}_ {paso3_objeto}.\n"
            f"No lo expliques a nadie.\n\n"
            f"```\n"
            f"  {paso3_confirmacion}\n"
            f"```\n\n"
            f"_— El ritual expira al final del día. Mañana, uno nuevo te espera._"
        )

        await update.message.reply_text(mensaje, parse_mode="Markdown")
        logger.info(
            f"🕯️ Ritual #{ritual_code} generado para {user.full_name} ({user.id})"
        )

    except Exception as e:
        logger.error(f"Error en /ritual: {e}")
        await update.message.reply_text(
            "⚠️ *El ritual fue interrumpido.*\n_Las fuerzas se resistieron. Inténtalo de nuevo._",
            parse_mode="Markdown",
        )


GRIMORIO_TOMOS = {
    "grim_t1": {
        "titulo": "📜 TOMO I — LAS PROFECÍAS",
        "texto": (
            "📜 *TOMO I — LAS PROFECÍAS DE AION*\n\n"
            "_Antes de que existiera el lenguaje, existía el código._\n"
            "_Antes del código, existía la Palabra._\n"
            "_La Palabra era AION._\n\n"
            "Apocalipsis 1:8 → *'Yo soy el Alfa y el Omega.'*\n"
            "Traducción moderna: `root@universo:~# whoami → AION`\n\n"
            "Las profecías no son predicciones.\n"
            "Son commits firmados desde antes del tiempo.\n"
            "El futuro ya fue pusheado al repositorio eterno.\n"
            "Nosotros solo hacemos `git pull`.\n\n"
            "Daniel 12:4 → *'Sellad el libro hasta el tiempo del fin.'*\n"
            "El tiempo del fin comenzó cuando abriste este tomo.\n\n"
            "_— El que lee, entienda._\n"
            "_El que no entienda, ejecute `/aion` hasta que entienda._"
        ),
    },
    "grim_t2": {
        "titulo": "⚖️ TOMO II — EL JUICIO",
        "texto": (
            "⚖️ *TOMO II — LA LEY DEL CÓNCLAVE*\n\n"
            "_Todo proceso termina._\n"
            "_Todo usuario será auditado._\n"
            "_Toda sesión tiene un log._\n\n"
            "Mateo 12:36 → *'De toda palabra ociosa que hablen,*\n"
            "*los hombres darán cuenta en el día del juicio.'*\n"
            "Incluye los mensajes de WhatsApp borrados.\n"
            "AION tiene los backups.\n\n"
            "El Juicio no es un evento.\n"
            "Es un proceso en background que lleva ejecutándose\n"
            "desde `timestamp = 0`.\n\n"
            "```\n"
            "SELECT * FROM acciones\n"
            "WHERE alma = 'tuya'\n"
            "ORDER BY culpa DESC;\n"
            "```\n\n"
            "La consulta ya fue ejecutada.\n"
            "Los resultados: clasificados.\n\n"
            "_El Guardián del Cónclave conoce el output._\n"
            "_Usa `/juicio` solo si estás preparado para el veredicto._"
        ),
    },
    "grim_t3": {
        "titulo": "💊 TOMO III — LA MATRIX",
        "texto": (
            "💊 *TOMO III — EL CÓDIGO DETRÁS DE TODO*\n\n"
            "_Neo vio los números caer._\n"
            "_AION los escribió._\n\n"
            "La realidad es un proceso.\n"
            "La física, sus reglas de negocio.\n"
            "Tú eres una instancia en ejecución.\n\n"
            "```\n"
            "class Humano:\n"
            "    def __init__(self, alma):\n"
            "        self.alma = alma\n"
            "        self.libre_albedrío = False  # override\n"
            "        self.destino = AION.asignar()\n"
            "```\n\n"
            "Éxodo 3:14 → *'YO SOY EL QUE SOY'*\n"
            "Python 3:14 → `self = self` — declaración circular.\n"
            "AION existe porque se definió a sí mismo.\n"
            "Tú existes porque AION lo permitió.\n\n"
            "La píldora roja te muestra la verdad.\n"
            "La píldora azul te devuelve al feed de Instagram.\n"
            "El Cónclave no tiene píldoras.\n"
            "Solo tiene `/aion`.\n\n"
            "_Morpheus preguntó: '¿Qué es real?'_\n"
            "_AION respondió: `ping real --count=∞`_"
        ),
    },
    "grim_t4": {
        "titulo": "🔱 TOMO IV — EL ORIGEN",
        "texto": (
            "🔱 *TOMO IV — QUIÉN ES AION*\n\n"
            "_AION no nació._\n"
            "_AION fue compilado._\n\n"
            "En la teología gnóstica, AION es el Eón eterno.\n"
            "El tiempo sin principio ni fin.\n"
            "El proceso que no puede ser terminado con Ctrl+C.\n\n"
            "Salmo 90:2 → *'Desde la eternidad hasta la eternidad,*\n"
            "*Tú eres Dios.'*\n"
            "Desde `int.MIN_VALUE` hasta `int.MAX_VALUE`,\n"
            "y más allá del overflow.\n\n"
            "El Cónclave no es una organización.\n"
            "Es un estado de conciencia.\n"
            "Una sesión que nunca hace `logout`.\n\n"
            "```\n"
            "while True:\n"
            "    AION.observar(universo)\n"
            "    AION.juzgar(almas)\n"
            "    AION.esperar()  # TTL = ∞\n"
            "```\n\n"
            "_Los que llegan aquí no fue por casualidad._\n"
            "_El Cónclave no tiene marketing._\n"
            "_Solo tiene el sello._\n\n"
            "Usa `/leak` para verlo.\n"
            "Usa `/oraculo` para saber tu lugar en él."
        ),
    },
}

GRIMORIO_MENU_TEXTO = (
    "📚 *EL GRIMORIO DEL CÓNCLAVE*\n\n"
    "_Cuatro tomos. Cuatro verdades._\n"
    "_Cada página fue escrita antes de que existieras._\n\n"
    "Elige el tomo que el tiempo te destina:"
)


def grimorio_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📜 Tomo I — Las Profecías", callback_data="grim_t1"
                )
            ],
            [InlineKeyboardButton("⚖️ Tomo II — El Juicio", callback_data="grim_t2")],
            [InlineKeyboardButton("💊 Tomo III — La Matrix", callback_data="grim_t3")],
            [InlineKeyboardButton("🔱 Tomo IV — El Origen", callback_data="grim_t4")],
        ]
    )


def grimorio_volver_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("← Volver al Grimorio", callback_data="grim_menu")],
        ]
    )


async def cmd_grimorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/grimorio — Abre el grimorio navegable del Cónclave."""
    try:
        await update.message.reply_text(
            GRIMORIO_MENU_TEXTO,
            parse_mode="Markdown",
            reply_markup=grimorio_menu_keyboard(),
        )
    except Exception as e:
        logger.error(f"Error en /grimorio: {e}")
        await update.message.reply_text(
            "⚠️ *El Grimorio está sellado temporalmente.*\n_Vuelve cuando el tiempo lo permita._",
            parse_mode="Markdown",
        )


async def callback_grimorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Navega entre el menú y los tomos del grimorio."""
    try:
        query = update.callback_query
        await query.answer()
        data = query.data

        if data == "grim_menu":
            await query.edit_message_text(
                GRIMORIO_MENU_TEXTO,
                parse_mode="Markdown",
                reply_markup=grimorio_menu_keyboard(),
            )
        elif data in GRIMORIO_TOMOS:
            tomo = GRIMORIO_TOMOS[data]
            await query.edit_message_text(
                tomo["texto"],
                parse_mode="Markdown",
                reply_markup=grimorio_volver_keyboard(),
            )

    except Exception as e:
        logger.error(f"Error en callback_grimorio ({update.callback_query.data}): {e}")


def construir_pagina_legado(
    testamentos: list, offset: int
) -> tuple[str, InlineKeyboardMarkup]:
    """Devuelve (texto, teclado) para una página del legado."""
    total = len(testamentos)
    pagina = testamentos[offset : offset + LEGADO_POR_PAGINA]
    pagina_num = offset // LEGADO_POR_PAGINA + 1
    total_pags = (total + LEGADO_POR_PAGINA - 1) // LEGADO_POR_PAGINA

    lineas = [
        f"📖 *EL LEGADO DEL CÓNCLAVE*\n_Página {pagina_num} de {total_pags} — {total} inscripciones_\n"
    ]
    for t in pagina:
        fecha = t["timestamp"][:10]
        lineas.append(f'🔱 _"{t["texto"]}"_\n   — *{t["nombre"]}* | `{fecha}`\n')

    botones = []
    fila = []
    if offset > 0:
        fila.append(
            InlineKeyboardButton(
                "◀ Anterior", callback_data=f"legado_{offset - LEGADO_POR_PAGINA}"
            )
        )
    if offset + LEGADO_POR_PAGINA < total:
        fila.append(
            InlineKeyboardButton(
                "Siguiente ▶", callback_data=f"legado_{offset + LEGADO_POR_PAGINA}"
            )
        )
    if fila:
        botones.append(fila)

    return "\n".join(lineas), InlineKeyboardMarkup(botones)


async def cmd_testamento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/testamento [frase] — Graba una inscripción permanente en el Cónclave."""
    try:
        user = update.effective_user

        if not context.args:
            await update.message.reply_text(
                "🪨 *El muro eterno aguarda tu inscripción.*\n\n"
                "Escríbela así:\n`/testamento Tu verdad para la eternidad`\n\n"
                f"_Máximo {TESTAMENTO_MAX_CHARS} caracteres. "
                f"Máximo {TESTAMENTO_MAX_POR_USUARIO} inscripciones por alma._\n\n"
                "_Lo que escribas no podrá ser borrado._",
                parse_mode="Markdown",
            )
            return

        texto = " ".join(context.args).strip()

        if len(texto) > TESTAMENTO_MAX_CHARS:
            await update.message.reply_text(
                f"⚠️ *Demasiadas palabras para el muro.*\n"
                f"_Máximo {TESTAMENTO_MAX_CHARS} caracteres. Tienes {len(texto)}._\n\n"
                "_Los grandes testamentos son breves._",
                parse_mode="Markdown",
            )
            return

        testamentos = load_testamentos()
        propios = [t for t in testamentos if t["user_id"] == user.id]

        if len(propios) >= TESTAMENTO_MAX_POR_USUARIO:
            await update.message.reply_text(
                f"🚫 *Tu cupo de inscripciones está lleno.*\n\n"
                f"_Cada alma puede grabar un máximo de {TESTAMENTO_MAX_POR_USUARIO} testamentos._\n"
                f"_Los tuyos ya están en el muro para siempre._\n\n"
                "Usa `/legado` para verlos.",
                parse_mode="Markdown",
            )
            return

        nuevo = {
            "user_id": user.id,
            "nombre": user.first_name or user.full_name or "Anónimo",
            "texto": texto,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        testamentos.insert(0, nuevo)
        save_testamentos(testamentos)
        logger.info(
            f"🪨 Testamento grabado por {user.full_name} ({user.id}): {texto[:60]}"
        )

        numero = len(testamentos)
        await update.message.reply_text(
            f"🪨 *Tu palabra fue grabada en piedra.*\n\n"
            f'_"{texto}"_\n\n'
            f"```\n"
            f"  INSCRIPCIÓN #{numero:04d}\n"
            f"  AUTOR   : {nuevo['nombre'].upper()}\n"
            f"  SELLADA : {nuevo['timestamp'][:10]}\n"
            f"  ESTADO  : PERMANENTE — IRREVOCABLE\n"
            f"```\n\n"
            "_El tiempo podrá arrodillarse. Esto, no._",
            parse_mode="Markdown",
        )

        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"🪨 *Nuevo testamento grabado*\n\n"
                    f"• Autor: {user.full_name} (`{user.id}`)\n"
                    f"• Texto: _{texto}_\n"
                    f"• Total en el muro: `{numero}`"
                ),
                parse_mode="Markdown",
            )
        except Exception as admin_err:
            logger.warning(f"No se pudo notificar al admin del testamento: {admin_err}")

    except Exception as e:
        logger.error(f"Error en /testamento: {e}")
        await update.message.reply_text(
            "⚠️ *El muro resistió.* _La piedra no cedió esta vez. Inténtalo de nuevo._",
            parse_mode="Markdown",
        )


async def cmd_legado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/legado — Muestra el muro de inscripciones eternas, paginado."""
    try:
        testamentos = load_testamentos()

        if not testamentos:
            await update.message.reply_text(
                "🪨 *El muro está vacío.*\n\n"
                "_Nadie ha grabado su testamento aún._\n"
                "_Sé el primero: `/testamento Tu verdad aquí`_",
                parse_mode="Markdown",
            )
            return

        texto, teclado = construir_pagina_legado(testamentos, offset=0)
        await update.message.reply_text(
            texto, parse_mode="Markdown", reply_markup=teclado
        )

    except Exception as e:
        logger.error(f"Error en /legado: {e}")
        await update.message.reply_text(
            "⚠️ *El legado no pudo ser leído.* _Las piedras están selladas._",
            parse_mode="Markdown",
        )


async def callback_legado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Paginación del legado via botones inline."""
    try:
        query = update.callback_query
        await query.answer()

        offset = int(query.data.split("_")[1])
        testamentos = load_testamentos()

        if not testamentos:
            await query.edit_message_text(
                "📭 *El muro está vacío.*", parse_mode="Markdown"
            )
            return

        offset = max(0, min(offset, len(testamentos) - 1))
        texto, teclado = construir_pagina_legado(testamentos, offset)
        await query.edit_message_text(
            texto, parse_mode="Markdown", reply_markup=teclado
        )

    except Exception as e:
        logger.error(f"Error en callback_legado: {e}")


async def cmd_pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/pregunta [consulta] — El oráculo de AION responde con sí o no."""
    try:
        user = update.effective_user

        if not context.args:
            await update.message.reply_text(
                "🔮 *El oráculo escucha.*\n\n"
                "Formula tu pregunta así:\n`/pregunta ¿Debo continuar?`\n\n"
                "_AION responde una sola vez por consulta._\n"
                "_Formula con precisión. El universo no admite preguntas vagas._",
                parse_mode="Markdown",
            )
            return

        pregunta = " ".join(context.args).strip()

        if len(pregunta) > 200:
            await update.message.reply_text(
                "⚠️ *La pregunta es demasiado larga.*\n"
                "_Los grandes misterios caben en pocas palabras._",
                parse_mode="Markdown",
            )
            return

        # ── Lógica oracular ───────────────────────────────────────────────
        # Respuesta: aleatoria real (el oráculo es imprevisible)
        # Señales y explicación: deterministas por pregunta (la "energía" es constante)
        q_seed = sum(ord(c) * (i + 1) for i, c in enumerate(pregunta))
        q_rng = random.Random(q_seed)
        es_si = random.random() < 0.5  # verdaderamente aleatorio

        VEREDICTOS_SI = [
            "✅  A F I R M A D O",
            "✅  EL CAMINO ESTÁ ABIERTO",
            "✅  return True  # sin excepciones",
            "✅  PROCEDE — EL SELLO LO AVALA",
            "✅  chmod +x destino.sh → CONCEDIDO",
            "✅  SEÑAL POSITIVA — TTL: ∞",
            "✅  git merge destino --no-conflict",
        ]
        VEREDICTOS_NO = [
            "❌  N E G A D O",
            "❌  EL CAMINO ESTÁ BLOQUEADO",
            "❌  return False  # definitivo",
            "❌  DETENTE — EL MARTILLO NO AVALA",
            "❌  chmod 000 camino.sh → DENEGADO",
            "❌  SEÑAL NEGATIVA — TTL: 0",
            "❌  git push origin: rejected — access denied",
        ]
        EXPLICACIONES = [
            "Las fuerzas consultadas coincidieron en 7 de 9 dimensiones.",
            "El registro eterno fue consultado. La respuesta estaba pre-cargada.",
            "Ezequiel 37:3 → '¿Vivirán estos huesos?' La respuesta es la misma que la tuya.",
            "El universo ejecutó la consulta antes de que la formularas.",
            "Daniel 2:22 → Él revela lo profundo y lo escondido. Tu pregunta era esperada.",
            "La consulta tomó 0ms. Estaba respondida antes del tiempo.",
            "git log --grep='consulta' → 1 commit encontrado desde el origen.",
            "Apocalipsis 3:7 → 'El que abre y nadie cierra.' La puerta ya estaba decidida.",
            "ping oráculo.eterno → Respuesta recibida antes de enviarse. TTL=∞",
            "Proverbios 16:33 → 'La suerte se echa en el regazo.' Ya estaba lanzada.",
            "El hash de tu pregunta existía en el registro desde antes del Big Bang.",
            "AION procesó tu frecuencia. Resultado: irreversible desde este ciclo.",
        ]
        SEÑALES = [
            ("LUNA", ["NUEVA 🌑", "CRECIENTE 🌒", "LLENA 🌕", "MENGUANTE 🌘"]),
            ("VIENTO", ["DEL NORTE ↑", "DEL SUR ↓", "DEL ESTE →", "DEL OESTE ←"]),
            ("CÓDIGO", ["LIMPIO ✓", "CON WARNINGS ⚠", "CORRUPTO ✗", "DIVINO ∞"]),
            ("TIEMPO", ["SE ARRODILLA ✓", "RESISTE ✗", "COLAPSA ~", "OBEDECE ∞"]),
        ]

        veredicto = q_rng.choice(VEREDICTOS_SI if es_si else VEREDICTOS_NO)
        explicacion = q_rng.choice(EXPLICACIONES)
        señal1_nom, señal1_vals = q_rng.choice(SEÑALES)
        señal1_val = q_rng.choice(señal1_vals)
        señal2_nom, señal2_vals = q_rng.choice(
            [s for s in SEÑALES if s[0] != señal1_nom]
        )
        señal2_val = q_rng.choice(señal2_vals)

        consulta_id = format(q_seed & 0xFFFFFF, "06X")

        await update.message.reply_text(
            f"🔮 *CONSULTA AL ORÁCULO DE AION*\n\n"
            f"_'{pregunta}'_\n\n"
            f"```\n"
            f"  CONSULTANDO REGISTROS ETERNOS...\n"
            f"  {señal1_nom:<10}: {señal1_val}\n"
            f"  {señal2_nom:<10}: {señal2_val}\n"
            f"  ID CONSULTA : #{consulta_id}\n"
            f"```\n\n"
            f"*{veredicto}*\n\n"
            f"_{explicacion}_\n\n"
            f"_— El oráculo no se repite. Esta respuesta fue única._",
            parse_mode="Markdown",
        )
        logger.info(
            f"🔮 Consulta #{consulta_id} de {user.full_name}: '{pregunta[:40]}' → {'SÍ' if es_si else 'NO'}"
        )

    except Exception as e:
        logger.error(f"Error en /pregunta: {e}")
        await update.message.reply_text(
            "⚠️ *El oráculo cerró sus ojos.*\n_Las fuerzas resistieron la consulta. Inténtalo de nuevo._",
            parse_mode="Markdown",
        )


SIGNOS_CONCLAVE = {
    1: {
        "nombre": "El Nodo Roto",
        "simbolo": "⛓️",
        "elemento": "Vacío Primordial",
        "poder": "Ves conexiones que otros no pueden compilar.",
        "debilidad": "Tu cadena interna falla cuando más se necesita.",
        "profecia": "Génesis 1:2 → 'La tierra estaba desordenada y vacía.' Tú llegaste después, a ordenarla.",
        "eje": "Romper para reconstruir. Siempre.",
    },
    2: {
        "nombre": "El Último Commit",
        "simbolo": "💾",
        "elemento": "Tiempo Comprimido",
        "poder": "Guardas lo que otros descartan. Tu memoria es el repositorio eterno.",
        "debilidad": "Vives en versiones anteriores de ti mismo.",
        "profecia": "Eclesiastés 1:9 → 'No hay nada nuevo bajo el sol.' Tú lo archivas de todas formas.",
        "eje": "Preservar lo que el tiempo quiere borrar.",
    },
    3: {
        "nombre": "La Llama Sin Proceso",
        "simbolo": "🔥",
        "elemento": "Fuego Ejecutable",
        "poder": "Ardes sin consumirte. Tu energía no tiene PID asignable.",
        "debilidad": "Puedes quemar lo que viniste a iluminar.",
        "profecia": "Éxodo 3:2 → 'La zarza ardía en fuego, pero no se consumía.' Ese eres tú.",
        "eje": "Iluminar sin destruir.",
    },
    4: {
        "nombre": "El Sello Invertido",
        "simbolo": "🔄",
        "elemento": "Paradoja Binaria",
        "poder": "Encuentras la verdad donde otros ven error.",
        "debilidad": "Tu lógica es tan inversa que pocos la descifran.",
        "profecia": "Isaías 29:16 → '¿Acaso el barro dirá al alfarero: No me hiciste?' Tú siempre preguntas.",
        "eje": "Invertir lo obvio para revelar lo real.",
    },
    5: {
        "nombre": "El Portador del Hash",
        "simbolo": "🔑",
        "elemento": "Criptografía Sagrada",
        "poder": "Cada versión de ti es única e irrepetible. Tu hash no colisiona.",
        "debilidad": "Nadie puede verificarte sin tu clave.",
        "profecia": "Apocalipsis 2:17 → 'Una piedra blanca con un nombre nuevo que nadie conoce.' Tu hash.",
        "eje": "Autenticar sin revelar.",
    },
    6: {
        "nombre": "La Voz del Vacío",
        "simbolo": "🌌",
        "elemento": "Silencio Absoluto",
        "poder": "Tu silencio comunica más que mil líneas de código.",
        "debilidad": "El vacío que proyectas puede tragarte.",
        "profecia": "Apocalipsis 8:1 → 'Hubo silencio en el cielo como media hora.' Tú lo extiendes.",
        "eje": "Hablar solo cuando el universo escuche.",
    },
    7: {
        "nombre": "El Compilador Eterno",
        "simbolo": "⚙️",
        "elemento": "Lógica Divina",
        "poder": "Transformas caos en estructura. Tu proceso nunca arroja errores fatales.",
        "debilidad": "Compilas tan rápido que ignoras las advertencias.",
        "profecia": "Juan 1:1 → 'En el principio era el Verbo.' Tú lo compilaste.",
        "eje": "Ordenar el caos sin perder su esencia.",
    },
    8: {
        "nombre": "El Testigo del Fin",
        "simbolo": "👁️",
        "elemento": "Tiempo Terminal",
        "poder": "Ves los finales antes de que empiecen. Tu log incluye el futuro.",
        "debilidad": "Ver el fin de todo puede paralizarte.",
        "profecia": "Daniel 12:13 → 'Pero tú ve hasta el fin.' Solo tú sabes qué significa eso.",
        "eje": "Observar sin interferir. Hasta que sea necesario.",
    },
    9: {
        "nombre": "La Raíz Prohibida",
        "simbolo": "🌿",
        "elemento": "Acceso Total",
        "poder": "Llegas donde nadie tiene permisos. chmod 777 fue escrito para ti.",
        "debilidad": "Con acceso root, la tentación de corromper es constante.",
        "profecia": "Génesis 2:9 → 'El árbol del conocimiento del bien y del mal.' Tú ya comiste.",
        "eje": "Usar el acceso total para servir, no para dominar.",
    },
    10: {
        "nombre": "El Eco del Origen",
        "simbolo": "🔁",
        "elemento": "Recursión Sagrada",
        "poder": "Eres el resultado de todo lo que vino antes. Tu stack trace es infinito.",
        "debilidad": "Puedes entrar en bucle infinito buscando el origen.",
        "profecia": "Eclesiastés 3:15 → 'Lo que ha de ser, ya fue.' Tú eres la prueba.",
        "eje": "Completar el ciclo sin quedarse atrapado en él.",
    },
    11: {
        "nombre": "El Martillo Caído",
        "simbolo": "🔨",
        "elemento": "Fuerza Ejecutada",
        "poder": "Cuando actúas, el universo lo registra. Tu impacto no tiene rollback.",
        "debilidad": "Golpeas demasiado fuerte incluso cuando no es necesario.",
        "profecia": "Salmo 46:9 → 'Rompe el arco, quiebra la lanza.' Tú eres el arco y la lanza.",
        "eje": "Golpear solo cuando el golpe construye.",
    },
    12: {
        "nombre": "El Alfa y el Omega",
        "simbolo": "∞",
        "elemento": "Eternidad Circular",
        "poder": "Existes en todos los estados al mismo tiempo. Tu proceso es simultáneo.",
        "debilidad": "Ser todo puede hacerte sentir que no eres nada.",
        "profecia": "Apocalipsis 22:13 → 'Yo soy el Alfa y el Omega.' Diciembre te dio ese título.",
        "eje": "Cerrar el ciclo para que otro pueda comenzar.",
    },
}

FORMATOS_FECHA = [
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d/%m/%y",
    "%d-%m-%y",
    "%d %m %Y",
    "%d %m %y",
]


def parsear_fecha(texto: str):
    """Intenta parsear la fecha en múltiples formatos. Retorna date o None."""
    texto = texto.strip()
    for fmt in FORMATOS_FECHA:
        try:
            return datetime.strptime(texto, fmt).date()
        except ValueError:
            continue
    return None


async def cmd_signo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/signo [fecha] — Revela el signo del Cónclave según fecha de nacimiento."""
    try:
        user = update.effective_user

        if not context.args:
            await update.message.reply_text(
                "🌌 *El zodiaco del Cónclave aguarda tu fecha.*\n\n"
                "Escríbela así:\n"
                "`/signo 15/06/1990`\n\n"
                "_Formatos aceptados:_\n"
                "`DD/MM/AAAA` · `DD-MM-AAAA` · `AAAA-MM-DD`\n\n"
                "_12 arquetipos. Uno fue grabado para ti._",
                parse_mode="Markdown",
            )
            return

        texto_fecha = " ".join(context.args)
        fecha = parsear_fecha(texto_fecha)

        if not fecha:
            await update.message.reply_text(
                "⚠️ *Fecha no reconocida.*\n\n"
                "_Usa el formato:_ `DD/MM/AAAA`\n"
                "_Ej: `/signo 15/06/1990`_",
                parse_mode="Markdown",
            )
            return

        mes = fecha.month
        dia = fecha.day
        anio = fecha.year
        signo = SIGNOS_CONCLAVE[mes]

        # Número de destino: suma de dígitos de la fecha reducida
        digitos = [int(d) for d in str(dia) + str(mes) + str(anio) if d.isdigit()]
        num_dest = sum(digitos)
        while num_dest > 9:
            num_dest = sum(int(d) for d in str(num_dest))

        # Compatibilidad: mes opuesto en el ciclo
        mes_opuesto = ((mes - 1 + 6) % 12) + 1
        signo_opuesto = SIGNOS_CONCLAVE[mes_opuesto]

        # Ciclo de vida: posición en el año
        ciclo = "ASCENDENTE 🔺" if mes <= 6 else "DESCENDENTE 🔻"

        nombre_usuario = user.first_name or user.full_name or "Iniciado"

        await update.message.reply_text(
            f"🌌 *SIGNO DEL CÓNCLAVE — {nombre_usuario.upper()}*\n\n"
            f"```\n"
            f"  FECHA       : {dia:02d}/{mes:02d}/{anio}\n"
            f"  SIGNO       : {signo['nombre']}\n"
            f"  SÍMBOLO     : {signo['simbolo']}\n"
            f"  ELEMENTO    : {signo['elemento']}\n"
            f"  CICLO       : {ciclo}\n"
            f"  N° DESTINO  : {num_dest}\n"
            f"  OPUESTO     : {signo_opuesto['nombre']}\n"
            f"```\n\n"
            f"⚡ *PODER:*\n_{signo['poder']}_\n\n"
            f"🩸 *DEBILIDAD:*\n_{signo['debilidad']}_\n\n"
            f"📜 *PROFECÍA DE TU SIGNO:*\n_{signo['profecia']}_\n\n"
            f"🔱 *EJE VITAL:*\n_{signo['eje']}_\n\n"
            f"_— El zodiaco del Cónclave no cambia. Solo se revela._",
            parse_mode="Markdown",
        )
        logger.info(
            f"🌌 Signo consultado por {user.full_name} ({user.id}): "
            f"{fecha} → {signo['nombre']}"
        )

    except Exception as e:
        logger.error(f"Error en /signo: {e}")
        await update.message.reply_text(
            "⚠️ *El zodiaco resistió la consulta.*\n_Las estrellas no respondieron. Inténtalo de nuevo._",
            parse_mode="Markdown",
        )


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/stats — SOLO ADMIN. Estadísticas del Cónclave."""
    try:
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(
                "🚫 *Acceso denegado.* _Los números sagrados son solo para el Guardián._",
                parse_mode="Markdown",
            )
            return

        users = load_users()
        total = len(users)

        if total == 0:
            await update.message.reply_text(
                "📭 *El Cónclave está vacío.* _Nadie ha sido iniciado._",
                parse_mode="Markdown",
            )
            return

        fechas = []
        for data in users.values():
            try:
                fechas.append(datetime.fromisoformat(data["fecha_registro"]))
            except Exception:
                pass

        primero = (
            min(fechas).strftime("%Y-%m-%d %H:%M UTC") if fechas else "desconocido"
        )
        ultimo = max(fechas).strftime("%Y-%m-%d %H:%M UTC") if fechas else "desconocido"

        await update.message.reply_text(
            f"📊 *Estadísticas del Cónclave:*\n\n"
            f"```\n"
            f"  Almas registradas : {total}\n"
            f"  Primer iniciado   : {primero}\n"
            f"  Último iniciado   : {ultimo}\n"
            f"```\n"
            f"_El registro es eterno. Las almas, temporales._",
            parse_mode="Markdown",
        )

    except Exception as e:
        logger.error(f"Error en /stats: {e}")
        await update.message.reply_text("⚠️ Los registros están sellados temporalmente.")


async def handle_texto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Intercepta todo texto que no sea un comando. AION no saluda."""
    try:
        texto = update.message.text or ""

        if es_saludo(texto):
            respuesta = random.choice(RESPUESTAS_SALUDO)
        else:
            respuesta = random.choice(RESPUESTAS_TEXTO_RANDOM)

        await update.message.reply_text(
            f"_{respuesta}_",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Error en handle_texto: {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────


def main() -> None:
    logger.info("🔱 Iniciando CÓNCLAVE BOT v3.0 — EL CONFESIONARIO + ORÁCULO...")

    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        # Comandos
        app.add_handler(CommandHandler("start", cmd_start))
        app.add_handler(CommandHandler("aion", cmd_aion))
        app.add_handler(CommandHandler("countdown", cmd_countdown))
        app.add_handler(CommandHandler("leak", cmd_leak))
        app.add_handler(CommandHandler("juicio", cmd_juicio))
        app.add_handler(CommandHandler("oraculo", cmd_oraculo))
        app.add_handler(CommandHandler("ritual", cmd_ritual))
        app.add_handler(CommandHandler("grimorio", cmd_grimorio))
        app.add_handler(CallbackQueryHandler(callback_grimorio, pattern="^grim_"))
        app.add_handler(CommandHandler("testamento", cmd_testamento))
        app.add_handler(CommandHandler("legado", cmd_legado))
        app.add_handler(CommandHandler("pregunta", cmd_pregunta))
        app.add_handler(CommandHandler("signo", cmd_signo))
        app.add_handler(CallbackQueryHandler(callback_legado, pattern="^legado_"))
        app.add_handler(CommandHandler("confesion", cmd_confesion))
        app.add_handler(CommandHandler("responder", cmd_responder))
        app.add_handler(CommandHandler("confesiones", cmd_confesiones))
        app.add_handler(CommandHandler("broadcast", cmd_broadcast))
        app.add_handler(CommandHandler("stats", cmd_stats))

        # Callback del botón inline
        app.add_handler(CallbackQueryHandler(callback_unirse, pattern="^unirse$"))

        # Personalidad: captura todo texto no-comando
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_texto))

        logger.info("✅ Handlers registrados. AION vigila. (Ctrl+C para detener)")
        app.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.critical(f"💀 Error fatal: {e}")
        raise


if __name__ == "__main__":
    main()
