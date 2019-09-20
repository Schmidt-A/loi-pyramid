import Templates from '../templates.js';
import { mockListener, mockTemplate, mockPage } from './__mocks__/templates.js';

let mockData1 = {'mockKey': 1};

test('new Listener()', () => {
	expect(mockListener).toBeTruthy();
	expect(mockListener.elementPath).toBe('div');
	expect(mockListener.eventType).toBe('click');
	//expect(mockListener.eventFunction).
});

test('new Template()', () => {
	expect(mockTemplate).toBeTruthy();
	//expect(mockTemplate.dataset).toBe('div');
	expect(mockTemplate.markup).toBe('<div></div>');
	//expect(mockTemplate.renderData).toBe('div');
	expect(mockTemplate.listeners[0]).toBe(mockListener);

});

/*test('new Page()', () => {
	expect(mockPage).toBeTruthy();
	expect(mockPage.container).toBe();
	expect(mockPage.path).toBeTruthy();
	expect(mockPage.markup).toBeTruthy();
	expect(mockPage.templateMap).toBeTruthy();

});*/