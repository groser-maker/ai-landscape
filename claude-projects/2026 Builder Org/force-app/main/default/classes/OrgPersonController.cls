public with sharing class OrgPersonController {

    @AuraEnabled(cacheable=true)
    public static List<OrgPerson__c> getAllPersons() {
        return [
            SELECT Id, Name, Title__c, Email__c,
                   Manager__c, Manager__r.Name,
                   Role__c, Type__c, SubType__c, Status__c,
                   Org62Id__c, PositionX__c, PositionY__c
            FROM OrgPerson__c
            ORDER BY Name ASC
            LIMIT 10000
        ];
    }

    @AuraEnabled
    public static void savePositions(List<OrgPerson__c> updates) {
        if (updates == null || updates.isEmpty()) return;
        update updates;
    }

    @AuraEnabled
    public static OrgPerson__c savePerson(OrgPerson__c person) {
        upsert person;
        return [
            SELECT Id, Name, Title__c, Email__c,
                   Manager__c, Manager__r.Name,
                   Role__c, Type__c, SubType__c, Status__c,
                   Org62Id__c, PositionX__c, PositionY__c
            FROM OrgPerson__c
            WHERE Id = :person.Id
        ];
    }

    @AuraEnabled(cacheable=true)
    public static Decimal getTargetOrgNumber() {
        OrgSettings__c settings = OrgSettings__c.getInstance();
        return settings != null ? settings.TargetOrgNumber__c : 0;
    }

    @AuraEnabled
    public static void saveTargetNumber(Decimal target) {
        OrgSettings__c settings = OrgSettings__c.getInstance();
        if (settings == null) {
            settings = new OrgSettings__c(
                SetupOwnerId = UserInfo.getOrganizationId()
            );
        }
        settings.TargetOrgNumber__c = target;
        upsert settings;
    }
}
