var cardProjectTemplate = _.template(
    '<div class="card">' +
      '<img class="card-img-top" src="<%= logo %>" alt="Card image cap">' +
      '<div class="card-body">' +
        '<h4 class="card-title"><%= project_name %></h4>' +
        '<p class="card-text"><%= project_description %></p>' +
        '<a href="<%= project_details %>" class="btn btn-primary">Learn more</a>' +
      '</div>' +
    '</div>');

// template for the projects
var projectTemplate = _.template(
    '<a href="<%= project_url %>" class="list-group-item list-group-item-action flex-column align-items-start">' +
        '<div class="d-flex w-100 justify-content-between">' +
            '<h5 class="mb-1"><%= project_name %></h5>' +
            '<small>updated <%= project_last_update %></small>' +
        '</div>' +
        '<p class="mb-1"><%= project_description %></p>' +
    '</a>');

// template for the organizations
var organizationTemplate = _.template(
    '<a href="<%= organization_url %>" class="list-group-item list-group-item-action flex-column align-items-start">' +
        '<div class="d-flex w-100 justify-content-between">' +
            '<h5 class="mb-1"><%= organization_name %></h5>' +
            '<small>updated <%= organization_last_update %></small>' +
        '</div>' +
        '<p class="mb-1"><%= organization_short_description %></p>' +
    '</a>');

// template for the users
var userTemplate = _.template(
    '<a href="<%= user_url %>" class="list-group-item list-group-item-action flex-column align-items-start">' +
        '<div class="d-flex w-100 justify-content-between">' +
            '<h5 class="mb-1"><%= user_login %></h5>' +
        '</div>' +
    '</a>');
