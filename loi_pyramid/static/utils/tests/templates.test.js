import Templates from '../templates.js';
import { mockListener, mockTemplate, mockContent, mockPage } from './__mocks__/templates.js';

let mockData1 = {'mockKey': 1};
let mockEvent = new Event('focus', { 'bubbles':false, 'cancelable':true });

beforeEach( () => {
    mockPage.container.innerHTML = '';
    mockContent.container.innerHTML = '';
    expect(mockContent.container.children.length).toBe(0);
    expect(mockPage.container.children.length).toBe(0);
});

test('new Listener()', () => {
    expect(mockListener).toBeTruthy();
    mockListener.eventFunction(mockEvent);

    expect(mockListener.elementPath).toBe('div');
    expect(mockListener.eventType).toBe('focus');
    expect(mockListener.eventFunction).toBeCalled();
});

test('new Template()', () => {
    expect(mockTemplate).toBeTruthy();
    mockTemplate.renderData();

    expect(mockTemplate.dataset).toBeTruthy();
    expect(mockTemplate.markup).toBe('<div class="mock"></div>');
    expect(mockTemplate.renderData).toBeCalled();
    expect(mockTemplate.listeners[0]).toBe(mockListener);
});

//Could this be a candidate for an integration test?
//Or at least to replace container with a non dom object
test('Template createContent()', () => {
    let newContainer = document.createElement('div');
    newContainer.id = 'newContent';
    document.body.appendChild(newContainer);

    let newContent = mockTemplate.createContent(newContainer);

    expect(newContent).toBeTruthy();
    newContent.renderData();

    expect(newContent.dataset).toBeTruthy();
    expect(newContent.markup).toBe('<div class="mock"></div>');
    expect(newContent.renderData).toBeCalled();
    expect(newContent.listeners[0]).toBe(mockListener);
    expect(newContent.container.id).toBe('newContent');
});

test('new Content()', () => {
    expect(mockContent).toBeTruthy();
    mockContent.renderData();

    expect(mockContent.dataset).toBeTruthy();
    expect(mockContent.markup).toBe('<div class="mock"></div>');
    expect(mockContent.renderData).toBeCalled();
    expect(mockContent.listeners[0]).toBe(mockListener);
    expect(mockContent.container.id).toBe('contentContainer');
});

test('Content renderMarkup()', () => {
    mockContent.renderMarkup();
    expect(mockContent.container.children[0].className).toBe('mock');
});

/* This is a candidate for an integration test, not a unit test because it is an event mechanism
test('Content addListeners()', () => {
    expect(mockContent.container.children.length).toBe(0);

    mockContent.renderMarkup();
    mockContent.addListeners();

    mockContent.container.children[0].focus();

    console.log(mockContent.listeners[0].eventFunction.mock);
    expect(mockContent.listeners[0].eventFunction).toBeCalled();
    
});*/

test('Content renderContent()', () => {
    mockContent.renderMarkup();
    mockContent.renderData();
    mockContent.addListeners();

    expect(mockContent.container.children[0].className).toBe('mock');
    expect(mockContent.renderData).toBeCalled();

    //purposely not testing the listeners here, those need to be integration
});

test('new Page()', () => {
    expect(mockPage).toBeTruthy();

    expect(mockPage.container.id).toBe('pageContainer');
    expect(mockPage.path).toBe('mock');
    expect(mockPage.markup).toBe(`<div id="sampleContent"></div>`);
    expect(mockPage.templateMap.sampleContent).toBe(mockTemplate);
});

//Using window pathname expectations here might be better for integration tests
test('Page render()', () => {
    mockPage.render();

    expect(mockPage.container.children[0].id).toBe('sampleContent');
    expect(mockPage.container.children[0].children[0].className).toBe('mock');

    expect(window.location.pathname).toBe('/app/mock');
});