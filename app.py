from rapidos.web import create_app


def run_flask():
    app = create_app()
    [print(repr(p)) for p in app.url_map.iter_rules()]

    app.run(debug=True)


if __name__ == '__main__':
    run_flask()
