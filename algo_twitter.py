NUMERO_INVALIDO = "Numero de tweet invalido."
SELECCION = "Seleccione una opcion:"
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS_MENSAJE = "Tweets eliminados:"
ATRAS = "**"
MENU = """Seleccione una opcion:

1. Crear Tweet
2. Buscar Tweet
3. Eliminar Tweet
4. Salir
"""


# -----------------------------------------------------------------------------


def main():
    """
    Funcion principal del programa.
    Ofrece las opciones hasta que se ingresa el numero 4.
    """
    id = 0
    tweets = {}
    tokens_ids = {}
    while True:
        opcion = input(MENU)
        if opcion == "1":
            nuevo_tweet = crear_tweet(id, tweets, tokens_ids)
            if nuevo_tweet:
                id += 1
            continue
        if opcion == "2":
            palabras_buscar = pedir_palabras(
                "Ingrese la/s palabra/s clave a buscar:\n"
            )
            buscar_tweet(palabras_buscar, tweets, tokens_ids)
            continue
        if opcion == "3":
            palabras_eliminar = pedir_palabras(
                "Ingrese el tweet a eliminar:\n"
            )
            eliminar_tweet(palabras_eliminar, tweets, tokens_ids)
            continue
        if opcion == "4":
            print(FIN)
            break
        print(INPUT_INVALIDO)


# -----------------------------------------------------------------------------


def verificar_ir_atras(opcion_input):
    """
    Recibe un string o un numero, devuelve un booleano segun la comparacion
    """
    return opcion_input == ATRAS


# -----------------------------------------------------------------------------


def crear_tweet(id, tweets, tokens_ids):
    """
    Recibe un string con la id del tweet, un diccionario de tweets,
    y un diccionario de tokens indexados.

    Pide el tweet, lo normaliza y lo agrega.
    Agrega los tokens del tweet al diccionario de tokens indexados.

    Devuelve un booleano dependiendo de si se agrego o no el tweet.
    """
    tweet_y_normalizado = pedir_tweet()
    if not tweet_y_normalizado:
        return False
    tweet, tweet_normalizado = tweet_y_normalizado
    agregar_tokens_indexados(id, tokens_ids, tweet_normalizado)
    tweets[id] = tweet
    print(f"OK {id}")
    return True


# -----------------------------------------------------------------------------


def pedir_tweet():
    """
    Pide un tweet hasta que se ingrese el numero 4
    o hasta que se ingrese un tweet valido.

    Devuelve el tweet ingresado y el normalizado en una tupla,
    o False si se ingreso 4.
    """
    while True:
        tweet = input("Ingrese el tweet a almacenar:\n")
        if verificar_ir_atras(tweet):
            return False
        tweet_normalizado = normalizar_texto(tweet)
        if not normalizar_texto(tweet):
            print(INPUT_INVALIDO)
            continue
        return (tweet, tweet_normalizado)


# -----------------------------------------------------------------------------


def normalizar_texto(texto):
    """
    Recibe un string y lo devuelve normalizado.
    """
    texto = texto.lower()
    tweet_normalizado = ""
    letras_con_tilde = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ä": "a",
        "ë": "e",
        "ï": "i",
        "ö": "o",
        "ü": "u",
    }
    for letra in texto:
        if not (letra.isalnum() or letra == " "):
            continue
        if letra in letras_con_tilde:
            tweet_normalizado += letras_con_tilde[letra]
            continue
        tweet_normalizado += letra
    return tweet_normalizado.strip()


# -----------------------------------------------------------------------------


def tokenizar_por_segmentos(palabras):
    """
    Recibe una lista de strings ya normalizados.

    Los tokeniza por segmentos de 3 letras como minimo
    y los agrega a una lista, si es de menos de 3 letras
    se agrega a la lista directamente.

    Devuelve la lista de segmentos.
    """
    segmentos = []
    for palabra in palabras:
        if len(palabra) > 3:
            for i in range(len(palabra)):
                longitud = i + 3
                while longitud <= len(palabra):
                    if palabra[i:longitud] not in segmentos:
                        segmentos.append(palabra[i:longitud])
                    longitud += 1
        else:
            segmentos.append(palabra)
    return segmentos


# -----------------------------------------------------------------------------


def agregar_tokens_indexados(id_tweet, tokens_ids, tweet_normalizado):
    """
    Recibe un string con la id del tweet, un diccionario de tokens indexados
    y un string normalizado.

    Tokeniza el tweet por segmentos y agrega cada segmento a la diccionario de
    tokens indexados, con su respectivo id.
    """
    palabras = tweet_normalizado.split()
    tokens = tokenizar_por_segmentos(palabras)
    for token in tokens:
        if token not in tokens_ids:
            tokens_ids[token] = [id_tweet]
        elif id_tweet not in tokens_ids[token]:
            tokens_ids[token].append(id_tweet)


# ---------------------------------------------------------------------------


def buscar_tweet(palabras, tweets, tokens_ids):
    """
    Recibe un string, un diccionario de tweets
    y un diccionario de tokens indexados.

    Busca las ids de los tweets que contienen esas palabras o segmentos.

    Devuelve un set con los ids encontrados o False si no se encontraron.
    """
    if not palabras:
        return False
    ids_resultantes = encontrar_tweets(palabras, tokens_ids)
    if not ids_resultantes:
        print(NO_ENCONTRADOS)
        return False
    mostrar_tweets(ids_resultantes, tweets)
    return ids_resultantes


# ---------------------------------------------------------------------------


def pedir_palabras(mensaje):
    """
    Recibe un string.

    Pide las palabras que se quieren buscar
    y las valida hasta que se ingresen correctamente o se ingrese el numero 4.

    Devuelve las palabras normalizadas y separadas en una lista
    o False si se ingresa el numero 4.
    """
    while True:
        palabras = input(mensaje)
        if verificar_ir_atras(palabras):
            return False
        palabras_normalizadas = normalizar_texto(palabras)
        if not palabras_normalizadas:
            print(INPUT_INVALIDO)
            continue
        return palabras_normalizadas.split()


# ---------------------------------------------------------------------------


def encontrar_tweets(palabras, tokens_ids):
    """
    Recibe una lista de string y un diccionario de tokens indexados.

    Verifica que cada palabra este en algun tweet.
    Busca los ids en comun.

    Devuelve el set con los ids resultantes,
    o False si la palabra no esta en ningun tweet
    o las palabras si estan pero en tweets diferentes.
    """
    ids_palabras = validar_palabras(palabras, tokens_ids)
    if not ids_palabras:
        return False
    ids_resultantes = encontrar_ids_comunes(ids_palabras)
    if not ids_resultantes:
        return False
    return ids_resultantes


# ---------------------------------------------------------------------------


def encontrar_ids_comunes(ids_palabras):
    """
    Recibe una lista de listas de ids.

    Agrega a una lista solo los ids que aparecen en todas las listas de ids
    y pasa la lista a un set para filtrar los ids repetidos.

    Devuelve el set con los ids resultantes
    o False si no hay ningun id en comun.
    """
    ids_resultantes = []
    if len(ids_palabras) == 1:
        return ids_palabras[0]
    for id in ids_palabras[0]:
        agregar = True
        for sub_id in ids_palabras[1:]:
            if id not in sub_id:
                agregar = False
                break
        if agregar:
            ids_resultantes.append(id)
    if not ids_resultantes:
        return False
    ids_resultantes = set(ids_resultantes)
    return ids_resultantes


# ---------------------------------------------------------------------------


def validar_palabras(palabras, tokens_ids):
    """
    Recibe una lista de strigs y un diccionario de tokens indexados.

    Verifica que cada palabra este en algun tweet, si estan todas,
    agrega a una lista los ids de los tweets
    en los que se encuentra cada palabra.

    Devuelve la lista con los ids
    o False si no encuentra alguna palabra
    """
    ids_palabras = []
    for palabra in palabras:
        if palabra not in tokens_ids:
            return False
        if tokens_ids[palabra] not in ids_palabras:
            ids_palabras.append(tokens_ids[palabra])
    return ids_palabras


# ---------------------------------------------------------------------------


def mostrar_tweets(ids, tweets):
    print(RESULTADOS_BUSQUEDA)
    for id in ids:
        print(f"{id}. {tweets[id]}")


# ---------------------------------------------------------------------------


def eliminar_tweet(palabras, tweets, tokens_ids):
    """
    Recibe un string, un diccionario de tweets y
    un diccionario de tokens indexados.

    Busca las palabras ingresadas, muestra los tweets encontrados,
    pide las ids de los tweets que se quieren eliminar, elimina los tweets
    y muestra los tweets eliminados.

    Devuelve un booleano dependiendo de si se encontro el tweet
    y si se borro o no.
    """
    tweets_encontrados = buscar_tweet(palabras, tweets, tokens_ids)
    if not tweets_encontrados:
        return False
    ids = pedir_ids(tweets)
    if not ids:
        return False
    tweets_eliminados = eliminar_tweet_e_ids_de_tokens(ids, tweets, tokens_ids)
    mostrar_tweets_eliminados(tweets_eliminados)
    return True


# ---------------------------------------------------------------------------


def pedir_ids(tweets):
    """
    Recibe un diccinario de tweets.

    Pide las ids de los tweets que se quieren eliminar
    y las valida hasta que se ingresen correctamente o se ingrese el numero 4.

    Devuelve un set con las ids normalizadas
    o False si se ingreso el numero 4.
    """
    while True:
        ids = input("Ingrese los numeros de tweets a eliminar:\n")
        if verificar_ir_atras(ids):
            return False
        ids = ids.split(",")
        ids_normalizadas = normalizar_ids(ids)
        if not ids_normalizadas:
            print(INPUT_INVALIDO)
            continue
        ids_normalizadas = set(ids_normalizadas)
        if not validar_ids(ids_normalizadas, tweets):
            print(NUMERO_INVALIDO)
            continue
        return ids_normalizadas


# ---------------------------------------------------------------------------


def normalizar_ids(ids):
    """
    Recibe un string con las id de los tweets que se quieren eliminar.

    Las normaliza y las devuelve en una lista,
    si no son validas devuelve False.
    """
    ids_normalizadas = []
    for i in range(len(ids)):
        if "-" in ids[i] and ids[i].count("-") == 1:
            rango = ids[i].split("-")
            num1 = rango[0].strip()
            num2 = rango[1].strip()
            if num1 <= num2 and num1.isnumeric() and num2.isnumeric():
                for sub_i in range(int(num1), int(num2) + 1):
                    ids_normalizadas.append(sub_i)
            else:
                return False
        elif not ids[i].strip().isnumeric():
            return False
        else:
            ids_normalizadas.append(int(ids[i]))
    return ids_normalizadas


# ---------------------------------------------------------------------------


def validar_ids(ids, tweets):
    """
    Recibe una lista con ids y un diccionario de tweets.

    Verifica que las ids existan.

    Devuelve un booleano dependiendo de si existen o no todas las ids.
    """
    for id in ids:
        if id not in tweets:
            return False
    return True


# ---------------------------------------------------------------------------


def eliminar_tweet_e_ids_de_tokens(ids, tweets, tokens_ids):
    """
    Recibe una lista con ids, un diccionario de tweets
    y un diccionario de token indexados.

    Agrega los tweets que va a eliminar a un diccionario
    con sus respectivos ids.
    Los elimina del diccionario de tweets
    y elimina los ids del tweet de los tokens a los que esta asociado.

    Devuelve el diccionario con los tweets eliminados.
    """
    tweets_eliminados = {}
    for id in ids:
        tweet_normalizado = normalizar_texto(tweets[id])
        palabras = tweet_normalizado.split()
        tokens = tokenizar_por_segmentos(palabras)
        tweets_eliminados[id] = tweets[id]

        for token in tokens:
            if len(tokens_ids[token]) > 1:
                tokens_ids[token].remove(id)
            else:
                tokens_ids.pop(token)
        tweets.pop(id)
    return tweets_eliminados


# ---------------------------------------------------------------------------


def mostrar_tweets_eliminados(tweets):
    print(TWEETS_ELIMINADOS_MENSAJE)
    for tweet in tweets:
        print(f"{tweet}. {tweets[tweet]}")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
