import templates from '../../templates.js'

export const mockEventFunction = jest.fn(event => {
  event.preventDefault()
})

export const mockListener = templates.listener(
  'div',
  'focus',
  mockEventFunction
)

export const mockTemplate = {
  markup: '<div class="mock"></div>',
  listeners: [mockListener],
  dataset: jest.mock('../../datasets.js'),
  renderData: jest.fn(() => { return Promise.resolve() })
}

export const mockPage = templates.page(
  'mock',
  '<div id="sampleContent"></div>',
  { sampleContent: mockTemplate }
)
