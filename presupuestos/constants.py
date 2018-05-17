class EstadoPresupuesto:
    PENDIENTE = 'PEN'
    REVISION = 'REV'
    APROBADO = 'APR'
    CONFIRMADO = 'CON'
    RECHAZADO = 'REC'

    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (REVISION, 'En revisión'),
        (APROBADO, 'Aprobado'),
        (CONFIRMADO, 'Confirmado o señado'),
        (RECHAZADO, 'Rechazado'),
    )
