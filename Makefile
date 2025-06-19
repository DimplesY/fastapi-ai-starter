.PHONY: migration migrate

migration:
	scripts/migration.sh

migrate: migration
	scripts/migrate.sh