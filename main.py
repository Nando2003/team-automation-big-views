from big_views import start
from big_views.types import FlowSpec
from big_views.widgets.text_step_widget import TextStepSpec, TextStepWidget
from time import sleep

def on_finish(ctx, logger):
    logger.info('Robô finalizado com sucesso!')
    sleep(10)  # Simula algum processamento final

flow = FlowSpec(
    name='Exemplo de Robô',
    steps=[
        TextStepSpec(
            key='user_input',
            title='Digite algo:',
            widget_cls=TextStepWidget,
            placeholder='Seu texto aqui...',
        )
    ],
    on_finish=[on_finish],
)

start(flow, window_title='Robô de Exemplo')
