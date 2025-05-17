--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-17 13:12:46

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5051 (class 0 OID 33517)
-- Dependencies: 224
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 5053 (class 0 OID 33525)
-- Dependencies: 226
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5049 (class 0 OID 33511)
-- Dependencies: 222
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, codename, content_type_id) FROM stdin;
1	Can add log entry	add_logentry	1
2	Can change log entry	change_logentry	1
3	Can delete log entry	delete_logentry	1
4	Can view log entry	view_logentry	1
5	Can add permission	add_permission	2
6	Can change permission	change_permission	2
7	Can delete permission	delete_permission	2
8	Can view permission	view_permission	2
9	Can add group	add_group	3
10	Can change group	change_group	3
11	Can delete group	delete_group	3
12	Can view group	view_group	3
13	Can add content type	add_contenttype	4
14	Can change content type	change_contenttype	4
15	Can delete content type	delete_contenttype	4
16	Can view content type	view_contenttype	4
17	Can add session	add_session	5
18	Can change session	change_session	5
19	Can delete session	delete_session	5
20	Can view session	view_session	5
21	Can add usuario	add_usuario	6
22	Can change usuario	change_usuario	6
23	Can delete usuario	delete_usuario	6
24	Can view usuario	view_usuario	6
25	Can add tarea	add_tarea	7
26	Can change tarea	change_tarea	7
27	Can delete tarea	delete_tarea	7
28	Can view tarea	view_tarea	7
29	Can add etiqueta	add_etiqueta	8
30	Can change etiqueta	change_etiqueta	8
31	Can delete etiqueta	delete_etiqueta	8
32	Can view etiqueta	view_etiqueta	8
33	Can add checklist item	add_checklistitem	9
34	Can change checklist item	change_checklistitem	9
35	Can delete checklist item	delete_checklistitem	9
36	Can view checklist item	view_checklistitem	9
37	Can add adjunto	add_adjunto	10
38	Can change adjunto	change_adjunto	10
39	Can delete adjunto	delete_adjunto	10
40	Can view adjunto	view_adjunto	10
41	Can add actividad	add_actividad	11
42	Can change actividad	change_actividad	11
43	Can delete actividad	delete_actividad	11
44	Can view actividad	view_actividad	11
\.


--
-- TOC entry 5061 (class 0 OID 33605)
-- Dependencies: 234
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 5047 (class 0 OID 33503)
-- Dependencies: 220
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	tareas	usuario
7	tareas	tarea
8	tareas	etiqueta
9	tareas	checklistitem
10	tareas	adjunto
11	tareas	actividad
\.


--
-- TOC entry 5045 (class 0 OID 33495)
-- Dependencies: 218
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-05-04 22:46:39.822585-05
2	auth	0001_initial	2025-05-04 22:46:39.904745-05
3	tareas	0001_initial	2025-05-04 22:46:39.963773-05
4	admin	0001_initial	2025-05-04 22:46:39.991738-05
5	sessions	0001_initial	2025-05-04 22:46:40.008601-05
6	tareas	0002_alter_usuario_options_alter_usuario_managers_and_more	2025-05-04 22:46:40.071418-05
7	tareas	0003_tarea	2025-05-05 14:53:40.86358-05
8	tareas	0004_alter_tarea_estado	2025-05-05 16:38:21.251153-05
9	tareas	0005_etiqueta_tarea_etiquetas	2025-05-05 19:11:34.86508-05
10	tareas	0006_usuario_pais	2025-05-05 22:04:02.648598-05
11	tareas	0007_usuario_ciudad	2025-05-05 22:35:23.139243-05
12	tareas	0008_checklistitem	2025-05-06 12:40:23.46347-05
13	tareas	0009_alter_checklistitem_tarea	2025-05-06 15:11:45.702171-05
14	tareas	0010_adjunto	2025-05-06 18:02:35.376937-05
15	tareas	0011_actividad	2025-05-06 19:07:46.700025-05
16	tareas	0012_usuario_fecha_nacimiento_usuario_genero_and_more	2025-05-07 16:28:12.404948-05
17	tareas	0013_alter_usuario_genero	2025-05-07 17:47:06.794258-05
\.


--
-- TOC entry 5062 (class 0 OID 33625)
-- Dependencies: 235
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- TOC entry 5074 (class 0 OID 33703)
-- Dependencies: 247
-- Data for Name: tareas_actividad; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_actividad (id, descripcion, fecha, tarea_id) FROM stdin;
1	Estado cambiado de 'finalizada' a 'en_progreso'	2025-05-06 19:20:01.60368-05	2
2	Estado cambiado de 'en_progreso' a 'completada'	2025-05-06 19:35:50.841263-05	2
3	La tarea fue actualizada por Natalia Nati	2025-05-08 18:08:43.489213-05	4
4	La tarea fue actualizada por Natalia Nati	2025-05-08 19:06:25.287005-05	4
\.


--
-- TOC entry 5072 (class 0 OID 33691)
-- Dependencies: 245
-- Data for Name: tareas_adjunto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_adjunto (id, archivo, descripcion, fecha_subida, tarea_id) FROM stdin;
\.


--
-- TOC entry 5070 (class 0 OID 33678)
-- Dependencies: 243
-- Data for Name: tareas_checklistitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_checklistitem (id, nombre, completado, fecha_creacion, tarea_id) FROM stdin;
1	Definir color del botón	t	2025-05-06 12:48:51.284325-05	1
3	Subtarea 2	t	2025-05-06 13:58:41.538181-05	3
2	Subtarea 1	t	2025-05-06 13:56:59.686583-05	3
\.


--
-- TOC entry 5066 (class 0 OID 33652)
-- Dependencies: 239
-- Data for Name: tareas_etiqueta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_etiqueta (id, nombre, color) FROM stdin;
1	inicio	gris
\.


--
-- TOC entry 5064 (class 0 OID 33638)
-- Dependencies: 237
-- Data for Name: tareas_tarea; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_tarea (id, titulo, descripcion, estado, prioridad, fecha_creacion, fecha_limite, asignado_a_id) FROM stdin;
1	Tarea actualizada con PUT	Nueva descripción para esta tarea	completada	media	2025-05-05 16:47:04.037543-05	2025-06-01	2
3	Tarea de prueba para checklist automático	Vamos a probar el cambio de estado automático	completada	media	2025-05-06 13:44:28.091427-05	\N	1
2	Primera tarea de prueba	Esta es una tarea actualizada	completada	alta	2025-05-05 20:51:01.741567-05	\N	1
4	Prueba	Cierre prueba	completada	baja	2025-05-08 17:16:16.040752-05	2025-05-23	5
\.


--
-- TOC entry 5068 (class 0 OID 33658)
-- Dependencies: 241
-- Data for Name: tareas_tarea_etiquetas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_tarea_etiquetas (id, tarea_id, etiqueta_id) FROM stdin;
1	2	1
\.


--
-- TOC entry 5055 (class 0 OID 33554)
-- Dependencies: 228
-- Data for Name: tareas_usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_usuario (id, password, last_login, is_superuser, email, is_staff, is_active, date_joined, nombre_completo, celular, foto, pais, ciudad, fecha_nacimiento, genero, numero_documento) FROM stdin;
2	pbkdf2_sha256$1000000$DTNiumK3smVnkYgLniqTqW$xRIlywAWRX4VQhSIlsmwgAVjUZwI08KZnY/Bd1MeB/Q=	\N	f	usuario@ejemplo.com	f	t	2025-05-04 23:06:46.46196-05	Usuario de Prueba			\N	\N	\N	\N	\N
1	pbkdf2_sha256$1000000$y5Z3avMHqV33i0pEVhZGBD$U/kZZ/RETWur1h9HShvJeNE/PrJNYtp9VDKt32WRnhA=	2025-05-06 17:20:12.471689-05	t	gestor@gmail.com	t	t	2025-05-04 22:48:28.11992-05	Juan Mejía	+573001112233	fotos_perfil/madrid.jpg	Colombia	Bogotá	\N	\N	\N
3	pbkdf2_sha256$1000000$WBXqxIz9LMPBpH39csyfsr$I/4lZmKb7t98YpVb9MYh3EqL+eXTfplv5ucwnRk/DIo=	\N	f	ferrr@gmail.com	f	t	2025-05-07 17:48:53.270291-05	Fernando	3213212323		Colombia	BOGOTA	1996-03-02	M	1023456789
5	pbkdf2_sha256$1000000$LBvMsXd6OTrBfcqZeFukyb$v69oSHSFFhR180HG9hfiMpCKZsQept8s7QL219hgmI0=	\N	f	nata1@gmail.com	f	t	2025-05-08 10:41:51.722568-05	Natalia Nati	3201234569	fotos_perfil/madrid_qK49kTW.jpg	Colombia	Medellin	1995-05-08	F	123456789
6	pbkdf2_sha256$1000000$VgC1CWI5D9wIVjNtvnU3Wd$vN3rJe7EMrcDrCQH+wyV7NaIZi8DapPh1T2Ts3Hou1Y=	\N	f	Pruebita@gmail.com	f	t	2025-05-13 21:16:37.298862-05	Pruebitas	3212330987		Colombia	BOGOTA DC	2002-02-22	M	2345678
\.


--
-- TOC entry 5057 (class 0 OID 33564)
-- Dependencies: 230
-- Data for Name: tareas_usuario_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_usuario_groups (id, usuario_id, group_id) FROM stdin;
\.


--
-- TOC entry 5059 (class 0 OID 33570)
-- Dependencies: 232
-- Data for Name: tareas_usuario_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tareas_usuario_user_permissions (id, usuario_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5081 (class 0 OID 0)
-- Dependencies: 223
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 5082 (class 0 OID 0)
-- Dependencies: 225
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 5083 (class 0 OID 0)
-- Dependencies: 221
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 44, true);


--
-- TOC entry 5084 (class 0 OID 0)
-- Dependencies: 233
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- TOC entry 5085 (class 0 OID 0)
-- Dependencies: 219
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 11, true);


--
-- TOC entry 5086 (class 0 OID 0)
-- Dependencies: 217
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 17, true);


--
-- TOC entry 5087 (class 0 OID 0)
-- Dependencies: 246
-- Name: tareas_actividad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_actividad_id_seq', 4, true);


--
-- TOC entry 5088 (class 0 OID 0)
-- Dependencies: 244
-- Name: tareas_adjunto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_adjunto_id_seq', 3, true);


--
-- TOC entry 5089 (class 0 OID 0)
-- Dependencies: 242
-- Name: tareas_checklistitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_checklistitem_id_seq', 3, true);


--
-- TOC entry 5090 (class 0 OID 0)
-- Dependencies: 238
-- Name: tareas_etiqueta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_etiqueta_id_seq', 1, true);


--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 240
-- Name: tareas_tarea_etiquetas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_tarea_etiquetas_id_seq', 1, true);


--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 236
-- Name: tareas_tarea_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_tarea_id_seq', 4, true);


--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 229
-- Name: tareas_usuario_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_usuario_groups_id_seq', 1, false);


--
-- TOC entry 5094 (class 0 OID 0)
-- Dependencies: 227
-- Name: tareas_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_usuario_id_seq', 6, true);


--
-- TOC entry 5095 (class 0 OID 0)
-- Dependencies: 231
-- Name: tareas_usuario_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_usuario_user_permissions_id_seq', 1, false);


-- Completed on 2025-05-17 13:12:46

--
-- PostgreSQL database dump complete
--

