from time import sleep
from typing import Unpack

from PySide6.QtWidgets import QLineEdit

from big_views import start
from big_views.types import FinishFnKwargs, FlowSpec
from big_views.widgets.form_step_widget import FormInput, FormStepSpec, FormStepWidget


def on_finish(context, logger, **kwargs):
    logger.info('Robô finalizado com sucesso!')
    sleep(3)  # Simula algum processamento final
    print('Contexto final:', context)
    print('Kwargs finais:', kwargs)
    status = kwargs.get('status')
    status('Robô finalizado com sucesso!')
    sleep(3)


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
