from time import sleep

from big_views import start
from big_views.types import FlowSpec
from big_views.widgets.text_step_widget import TextStepSpec, TextStepWidget
from big_views.widgets.form_step_widget import FormStepSpec, FormStepWidget, FormInput
from PySide6.QtWidgets import QLineEdit

def on_finish(ctx, logger):
    logger.info('Robô finalizado com sucesso!')
    sleep(10)  # Simula algum processamento final

flow = FlowSpec(
    name='Exemplo de Robô',
    steps=[
        FormStepSpec(
            key='login_step',
            title='Login',
            inputs=[
                FormInput(
                    key='username',
                    label='Nome de Usuário',
                    placeholder='Digite seu nome de usuário',
                ),
                FormInput(
                    key='password',
                    label='Senha',
                    placeholder='Digite sua senha',
                    echo_mode=QLineEdit.EchoMode.Password,
                ),
            ],
            widget_cls=FormStepWidget,
        )
    ],
    on_finish=[on_finish],
)

start(flow, window_title='Robô de Exemplo')
