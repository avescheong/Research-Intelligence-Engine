# Pluggable RIE Domain Modules

Drop any custom domain pack into this folder as a subfolder containing domain_module.json.
RIE auto-discovers and registers enabled domain modules at startup without modifying core engine code.

To create a private module (e.g., for personal projects):
1. Create a folder modules/private_<my_project>/
2. Add domain_module.json conforming to engine/core/schemas/domain_module.schema.json
3. Notice that .gitignore automatically excludes modules/private_*/ so private modules are never committed to public repositories.
