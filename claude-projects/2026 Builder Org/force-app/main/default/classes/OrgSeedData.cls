public without sharing class OrgSeedData {

    public class PersonSeed {
        public String name;
        public String title;
        public String email;
        public String org62Id;
        public String managerOrg62Id;
        public String role;
        public String type;
        public String subType;
        public String status;
    }

    public static void loadFromStaticResource() {
        StaticResource sr = [
            SELECT Body FROM StaticResource WHERE Name = 'orgSeedData' LIMIT 1
        ];
        String jsonBody = sr.Body.toString();
        List<PersonSeed> seeds = (List<PersonSeed>) JSON.deserialize(jsonBody, List<PersonSeed>.class);

        // First pass: upsert all persons without manager to establish IDs
        List<OrgPerson__c> firstPass = new List<OrgPerson__c>();
        for (PersonSeed s : seeds) {
            firstPass.add(new OrgPerson__c(
                Name = s.name,
                Title__c = s.title,
                Email__c = s.email,
                Org62Id__c = s.org62Id,
                Role__c = s.role,
                Type__c = s.type,
                SubType__c = s.subType,
                Status__c = (s.status != null ? s.status : 'In-Seat')
            ));
        }
        upsert firstPass Org62Id__c;

        // Build lookup map by Org62Id
        Map<String, Id> idByOrg62Id = new Map<String, Id>();
        for (OrgPerson__c p : [SELECT Id, Org62Id__c FROM OrgPerson__c WHERE Org62Id__c != null]) {
            idByOrg62Id.put(p.Org62Id__c, p.Id);
        }

        // Second pass: set manager relationships
        List<OrgPerson__c> secondPass = new List<OrgPerson__c>();
        for (PersonSeed s : seeds) {
            if (String.isNotBlank(s.managerOrg62Id) && idByOrg62Id.containsKey(s.org62Id) && idByOrg62Id.containsKey(s.managerOrg62Id)) {
                secondPass.add(new OrgPerson__c(
                    Id = idByOrg62Id.get(s.org62Id),
                    Manager__c = idByOrg62Id.get(s.managerOrg62Id)
                ));
            }
        }
        if (!secondPass.isEmpty()) {
            update secondPass;
        }
    }
}
