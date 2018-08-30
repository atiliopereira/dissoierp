class EstadoPresupuesto:
    BORRADOR = 'BOR'
    REVISADO = 'REV'
    ENVIADO = 'ENV'
    APROBADO = 'APR'
    RECHAZADO = 'REC'
    TERMINADO = 'TER'
    ESTADOS = (
        (BORRADOR, 'Borrador'),
        (REVISADO, 'Revisado'),
        (ENVIADO, 'Enviado al cliente'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (TERMINADO, 'Trabajo terminado')
    )