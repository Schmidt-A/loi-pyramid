import Templates from '../../templates.js';
import mockDataset from './datasets.js';

let mockData1 = {'mockKey': 1};

export const mockListener = new Templates.Listener(
	'div',
	'click',
	jest.fn( event => {
		event.preventDefault();
	})
);

export const mockTemplate = new Templates.Template(
	mockDataset,
	`<div></div>`,
	jest.fn( () => {
		mockDataset.getData(mockData1).then( mockGetData => {
			document.querySelector(`#${this.container.id} div`).value = mockGetData.mockKey	
		})
	}),
	[mockListener]
);

/*const sampleContent = new Templates.Content(
	 mockTemplate.dataset,
	 mockTemplate.markup,
	 mockTemplate.renderData,
	 mockTemplate.mockListener,
	 //
);*/

/*export const mockPage = new Templates.Page(
	//,
	'mock'
	`<div id="mockContent></div>"`,
	{ 'mockContent': mockTemplate }
);*/