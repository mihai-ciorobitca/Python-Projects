from argparse import ArgumentParser
from os import path
from importlib.util import (
    spec_from_file_location,
    module_from_spec,
)

def create_template(template_name):
    template_path = f"templates/{template_name}.py"
    
    if path.exists(template_path):
        print(f"Script '{template_name}.py' already exists.")
        return
    
    with open("templates/template.txt") as reader:
        template_content = reader.read()

    template_content = template_content.replace("Classname", template_name.capitalize())

    with open(template_path, "w") as writer:
        writer.write(template_content)

    print(f"Template '{template_name}.py' created successfully.")


def call_template(template):
    classname = template.capitalize()
    template_path = path.join("templates", f"{template}.py")
    if path.exists(template_path):
        spec = spec_from_file_location(template, template_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        template_class = getattr(module, classname, None)

        if template_class:
            template_instance = template_class()
            template_instance.run_bot()
        else:
            print(f"Class '{classname}' not found in template '{template}'")
    else:
        print(f"Template '{template}' not found")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="""
                    create Create a new template
                    call   Call an existing template
                    """
    )
    parser.add_argument("action", choices=["create", "call"])
    parser.add_argument("template", help="Argument for calling template")

    args = parser.parse_args()

    if args.action == "create":
        create_template(args.template)
    elif args.action == "call":
        call_template(args.template)
