from time import sleep

from big_views import start
from big_views.types import FlowSpec
from big_views.widgets.file_step_widget import FileStepSpec, FileStepWidget
from big_views.widgets.text_step_widget import TextStepSpec, TextStepWidget


def on_finish(context, logger, **kwargs):
    logger.info('Robô finalizado com sucesso!')
    sleep(3)  # Simula algum processamento final
    print('Contexto final:', context)
    print('Kwargs finais:', kwargs)
    sleep(3)


flow = FlowSpec(
    name='Exemplo de Robô',
    steps=[
        FileStepSpec(
            key='input_file',
            title='Selecione um arquivo de entrada',
            help_text='Por favor, escolha o arquivo que deseja processar.',
            dialog_title='Escolha o arquivo de entrada',
            file_filter='Text Files (*.txt);;All Files (*)',
            widget_cls=FileStepWidget,
        ),
        TextStepSpec(
            key='comments',
            title='Comentários adicionais',
            placeholder='Insira quaisquer comentários adicionais aqui...',
            widget_cls=TextStepWidget,
        ),
    ],
    on_finish=[on_finish],
)

start(flow, window_title='Robô de Exemplo')
