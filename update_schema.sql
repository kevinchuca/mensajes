-- Agrega la columna delivered_at si no existe
ALTER TABLE shipment ADD COLUMN IF NOT EXISTS delivered_at DATETIME NULL;
-- Nota: algunos MySQL no soportan IF NOT EXISTS para ALTER TABLE, en ese caso ejecutar:
-- ALTER TABLE shipment ADD COLUMN delivered_at DATETIME NULL;
