import Templates from '../../templates.js';
import { Dataset } from '../../datasets.js';

let mockData1 = {'mockKey': 1};

//the practice of using the dom for these unit mocks is possibly
let mockPageContainer = document.createElement('div');
mockPageContainer.id = 'pageContainer';
document.body.appendChild(mockPageContainer);
let mockContentContainer = document.createElement('div');
mockContentContainer.id = 'contentContainer';
document.body.appendChild(mockContentContainer);

export const mockListener = new Templates.Listener(
    'div',
    'focus',
    jest.fn( event => {
        event.preventDefault();
    })
);

export const mockTemplate = new Templates.Template(
    jest.mock('../../datasets.js'),
    `<div class="mock"></div>`,
    jest.fn( () => {}),
    [mockListener]
);

export const mockContent = new Templates.Content(
     mockTemplate.dataset,
     mockTemplate.markup,
     mockTemplate.renderData,
     mockTemplate.listeners,
     mockContentContainer
);

export const mockPage = new Templates.Page(
    mockPageContainer,
    'mock',
    `<div id="sampleContent"></div>`,
    { 'sampleContent': mockTemplate }
);