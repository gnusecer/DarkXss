DarkXss.factory('Project', function(Restangular) {
    var Project;
    Project = {
        get: function() {
            return Restangular
                .one('projects')
                .getList();
        },
        create: function(data) {
            return Restangular
                .one('projects')
                .customPOST(data);
        }
    };
    return Project;
})